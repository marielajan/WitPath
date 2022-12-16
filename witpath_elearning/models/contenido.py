from odoo import models, fields, api


class Contenido(models.Model):
    _name = 'wp.contenido'
    _description = 'contenido'

    orden = fields.Integer(string="Orden", required=True)
    titulo = fields.Char(string="Titulo", required=True)
    formato = fields.Selection(
        [('pdf', 'Documento'),
         ('pptx', 'Presentacion'),
         ('docx', 'Evaluacion'),
         ('avi', 'Video'),
         ('docx', 'Actividad')],
        default='pdf')
    contenido = fields.Binary(string='Adjuntar archivo')

    state = fields.Selection(
        [('activo', 'Activo'),
         ('inactivo', 'Inactivo')],
        default='inactivo', string="Estado")

    # relaciones entre tablas
    clase_id = fields.Many2one(comodel_name='wp.clases', string='Clase')

    def btn_activar(self):
        self.state = 'activo'

    def btn_desactivar(self):
        self.state = 'inactivo'