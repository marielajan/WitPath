from odoo import models, fields, api


class Cursos(models.Model):
    _name = 'wp.cursos'
    _description = 'cursos'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    image = fields.Binary(string="Imagen", attachment=True)
    name = fields.Char(string="Titulo", required=True, tracking=True)
    subtitulo = fields.Char(string="Subtitulo", required=True)
    tema = fields.Char(string="Tema", required=True)
    descripcion = fields.Char(string="Descripcion", required=True)
    fecha_inicio = fields.Date(string='Fecha de inicio')
    fecha_fin = fields.Date(string='Fecha de finalizacion')
    dias_cursado = fields.Char(string="Dias de cursado")
    horario_inicio = fields.Float(string="Horario de inicio")
    horario_finalizacion = fields.Float(string="Horario de finalizacion")
    state = fields.Selection([('activo', 'Activo'), ('inactivo', 'Inactivo')], default='activo', string="Estado")
    precio = fields.Float(string="Precio")

    # relaciones entre tablas
    clase_line_ids = fields.One2many('wp.clases', 'curso_id', 'Clases')
    alumno_line_ids = fields.Many2many(comodel_name='wp.alumnos', string='Alumnos')
    foro_line_ids = fields.One2many('wp.foros', 'curso_id', 'Foros')

    def btn_activar(self):
        self.state = 'activo'

    def btn_desactivar(self):
        self.state = 'inactivo'
