from odoo import models, fields


class Clases(models.Model):
    _name = 'wp.clases'
    _description = 'clases'

    name = fields.Char(string="Titulo", required=True)
    orden = fields.Integer(string="Orden", required=True)
    duracion = fields.Float(string="Duracion")
    state = fields.Selection(
        [('activo', 'Activo'),
         ('inactivo', 'Inactivo')],
        default='inactivo', string="Estado")

    # relaciones entre tablas
    curso_id = fields.Many2one(comodel_name='wp.cursos', string='Curso')
    contenido_line_ids = fields.One2many('wp.contenido', 'clase_id', string='Contenido')

    def btn_activar(self):
        self.state = 'activo'

    def btn_desactivar(self):
        self.state = 'inactivo'

