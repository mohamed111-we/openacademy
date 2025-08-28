from odoo import models, fields, api


class Wizard(models.TransientModel):
    _name = 'openacademy.wizard'
    _description = "Wizard: Quick Registration of Attendees to Sessions"

    def _default_sessions(self):
        res = self.env['openacademy.session'].browse(self._context.get('active_ids'))
        return res

    session_ids = fields.Many2many('openacademy.session', string="Sessions", required=True, default=_default_sessions,
                                   readonly=1)
    attendees_ids = fields.Many2many('res.partner', string="Attendees")

    # def subscribe(self):
    #     print('subscribe')
    #     print(self.session_ids.ids)
    #     print(self.session_ids.attendees_ids)
    #     self.session_ids.attendees_ids |= self.attendees_ids

    def subscribe(self):
        for session in self.session_ids:
            session.attendees_ids |= self.attendees_ids

