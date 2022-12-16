from odoo import models, fields, api


class Contratos(models.Model):
    _name = 'wp.contratos'
    _description = 'contratos'

    fecha_inicio = fields.Date('Fecha de inicio')
    fecha_fin = fields.Date('Fecha de finalizacion')
    cantidad_alumnos = fields.Integer('Cantidad Alumnos')
    importe = fields.Float('Importe')

    cliente = fields.Char(string='Cliente')
    cuit = fields.Char(string='Cuit', readonly=True)
    direccion = fields.Char(string='Direccion', readonly=True)
    telefono = fields.Char(string='Telefono', readonly=True)
    email = fields.Char(string='Email', readonly=True)

    # relaciones entre tablas
    cliente_id = fields.Many2one(comodel_name='wp.clientes', string='Cliente')
    cotizacion_id = fields.Many2one(comodel_name='wp.cotizaciones', string='Cotizacion')

    # def btn_get_context(self):
    #    cont = self.search_read([('cotizacion_id', '=', self._context['cot_id'])])
    #     print(cont[0]['id'])
    #    self.importe = cont[0]['importe']

    # @api.model
    # def default_get(self):
        #     cont = self.search_read([('cotizacion_id', '=', self._context['cot_id'])])
        # print(cont[0]['id'])
        # res = super()
        # res.update(cont[0])
        # return res
