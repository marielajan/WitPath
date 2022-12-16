from odoo import models, fields, api
# from odoo.exceptions import ValidationError


class Contactos(models.Model):
    _name = 'wp.contactos'
    _description = 'contactos'

    nombre = fields.Char(string="Nombre")
    email = fields.Char(string="Email")
    area = fields.Char(string="Area")
    funcion = fields.Char(string="Funcion")
    telefono = fields.Char(string="Telefono")

    # relaciones entre tablas
    cliente_id = fields.Many2one(comodel_name='wp.clientes', string='Cliente')

    # decorador para validar el formato de email
    # @api.constrains('email')
    # def validate_email(self):
    #    if self.email:
    #        match = re.match('^[_a-z]+[0-9-]*(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.email)
    #        if match is None:
    #            raise ValidationError('No es un email valido')
