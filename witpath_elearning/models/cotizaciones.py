from odoo import models, fields, api
from datetime import datetime, timedelta


class Cotizaciones(models.Model):
    _name = 'wp.cotizaciones'
    _description = 'cotizaciones'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    id = fields.Integer(string='Nro. Cotizacion', readonly=True)
    fecha_emision = fields.Date('Fecha emision', default=datetime.today(), readonly=True)
    fecha_aceptacion = fields.Date('Fecha de aceptacion')
    fecha_vigencia = fields.Date('Fecha de vigencia')
    state = fields.Selection(
        [('pendiente', 'Pendiente'),
         ('aceptada', 'Aceptada'),
         ('vencida', 'Vencida'),
         ('cancelada', 'Cancelada'),
         ('contratada', 'Contratada')],
        default='pendiente')
    cantidad_cursos = fields.Integer('Cantidad Cursos')
    cantidad_alumnos = fields.Integer('Cantidad Alumnos')
    importe = fields.Float('Importe ($)')
    iva = fields.Float('IVA (21%)')
    total = fields.Float('Total')
    descuento = fields.Float('Descuento (%)')
    cliente_id = fields.Integer(string='Cliente_id', related='cliente.id', readonly=True)
    cuit = fields.Char(string='Cuit', related='cliente.cuit', readonly=True)
    direccion = fields.Char(string='Direccion', related='cliente.direccion', readonly=True)
    telefono = fields.Char(string='Telefono', related='cliente.telefono', readonly=True)
    email = fields.Char(string='Email', related='cliente.email', readonly=True)

    # relaciones entre tablas
    cliente = fields.Many2one(comodel_name='wp.clientes', string='Cliente')
    cursos_id = fields.Many2many(comodel_name='wp.cursos', string='Cursos')
    cotizacion_detalle_line_ids = fields.One2many('wp.cotizaciones_detalle', 'cotizacion_id', 'Detalle')
    contrato_line_ids = fields.One2many('wp.contratos', 'cotizacion_id', 'Contratos')

    # Funciones
    @api.onchange("fecha_aceptacion")
    def _onchange_fecha_aceptacion(self):
        if self.fecha_emision and self.fecha_aceptacion:
            if self.cantidad_cursos == 0:
                self.fecha_aceptacion = ''
                return {
                    'warning': {
                        'title': '¡Advertencia!',
                        'message': 'No se puede aceptar una cotizacion sin cursos cargados'}
                }
            vencimiento = self.fecha_emision + timedelta(days=10)
            if self.fecha_aceptacion <= vencimiento:
                self.state = "aceptada"
            else:
                self.state = "vencida"

    @api.onchange("fecha_emision")
    def _onchange_fecha_vigencia(self):
        if self.fecha_emision:
            self.fecha_vigencia = self.fecha_emision + timedelta(days=10)

    def _calculos(self):
        self.iva = 0.00
        self.total = 0.00
        importeConDesc = (self.importe - self.descuento * self.importe / 100)
        self.iva = importeConDesc * 21 / 100
        self.total = importeConDesc + self.iva

    @api.onchange("cotizacion_detalle_line_ids")
    def _onchange_cotizacion_detalle_line_ids(self):
        self.importe = 0.00
        self.cantidad_cursos = 0
        self.cantidad_alumnos = 0
        for item in self.cotizacion_detalle_line_ids:
            self.importe = self.importe + item.subtotal
            self.cantidad_cursos += 1
            self.cantidad_alumnos = self.cantidad_alumnos + item.cantidad
        self._calculos()

    @api.onchange("descuento")
    def _onchange_descuento(self):
        if self.descuento > 100.00:
            self.descuento = 0.00
            return {
                'warning': {
                    'title': '¡Advertencia!',
                    'message': 'El porcentaje no puede ser mayor al 100%'}
            }
        if self.descuento < 0.00:
            self.descuento = 0.00
            return {
                'warning': {
                    'title': '¡Advertencia!',
                    'message': 'El porcentaje no puede ser menor que 0.00%'}
            }
        if self.importe and self.descuento:
            self._calculos()

    def btn_cancelar(self):
        self.state = 'cancelada'

    def btn_emitir_contrato(self):
        # Creo diccionario para guardar registro del contrato
        dic = {
            'fecha_inicio': self.fecha_aceptacion,
            'fecha_fin': self.fecha_emision,
            'cantidad_alumnos': self.cantidad_alumnos,
            'importe': self.total,
            'cliente_id': self.cliente_id,
            'cotizacion_id': self.id,
            'cliente': self.cliente.name,
            'cuit': self.cuit,
            'direccion': self.direccion,
            'telefono': self.telefono,
            'email': self.email
        }
        # Guardo el registro
        self.env['wp.contratos'].create(dic)
        self.state = 'contratada'
        return {
            'warning': {
                'title': 'Contrato',
                'message': 'Se emitio el contrato para la cotizacion'}
        }