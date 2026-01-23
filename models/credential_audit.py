from odoo import api, fields, models
from odoo.exceptions import AccessError


class CredentialAccessLog(models.Model):
    _name = 'sm.credential.access.log'
    _description = 'Credential Access Log'

    credential_id = fields.Many2one('sm.credential', string='Credential', required=True, ondelete='cascade')
    user_id = fields.Many2one('res.users', string='User', required=True, default=lambda self: self.env.user)
    action = fields.Selection([('reveal', 'Reveal'), ('copy', 'Copy')], string='Action', required=True)
    create_date = fields.Datetime(string='Access Time', readonly=True)


class CredentialRevealWizard(models.TransientModel):
    _name = 'sm.credential.reveal.wizard'
    _description = 'Credential Reveal Wizard'

    password = fields.Char(string='Password/Secret')

    def action_close(self):
        return {'type': 'ir.actions.act_window_close'}
