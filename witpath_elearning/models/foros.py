from odoo import models, fields, api


class Foros(models.Model):
    _name = 'wp.foros'
    _description = 'foros'

    orden = fields.Integer(string="Orden", required=True)
    titulo = fields.Char(string="Titulo", required=True)
    state = fields.Selection(
        [('activo', 'Activo'),
         ('inactivo', 'Inactivo')],
        default='activo')
    descripcion = fields.Char(string="Descripcion", required=True)

    # relaciones entre tablas
    clase_id = fields.Many2one(comodel_name='wp.clases', string='Clase')
    curso_id = fields.Many2one(comodel_name='wp.cursos', string='Curso')

    def btn_activar(self):
        self.state = 'activo'

    def btn_desactivar(self):
        self.state = 'inactivo'