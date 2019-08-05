from __future__ import unicode_literals

from django.apps import AppConfig, apps
from django.conf import settings

from esipy import App, EsiClient, EsiSecurity

class EveOnlineConfig(AppConfig):
    name = 'modules.eveonline'
    static_database = ''

    # APP CONFIG
    ALLIANCE_MODE = False

    # ESI STATIC VARIABLE
    ESI_APP = None # set at runtime

    # ESI INFORMATION
    ESI_APP_URL = "https://esi.evetech.net/latest/swagger.json?datasource=tranquility"
    ESI_CALLBACK_URL = settings.SERVER_DOMAIN + '/eve/sso/callback'

    # ESI USER SETTINGS
    ESI_CLIENT_ID = ''
    ESI_SECRET_KEY = ''

    # USER SETTINGS
    ESI_SCOPES = [
        'publicData',
        'esi-contracts.read_character_contracts.v1',
        'esi-location.read_location.v1',
        'esi-location.read_ship_type.v1',
        'esi-mail.read_mail.v1',
        'esi-skills.read_skills.v1',
        'esi-skills.read_skillqueue.v1',
        'esi-wallet.read_character_wallet.v1',
        'esi-characters.read_contacts.v1',
        'esi-corporations.read_corporation_membership.v1',
        'esi-assets.read_assets.v1',
        'esi-clones.read_clones.v1',
        'esi-fleets.read_fleet.v1',
        'esi-fleets.write_fleet.v1',
        'esi-characters.read_chat_channels.v1',
        'esi-industry.read_character_jobs.v1',
        'esi-markets.read_character_orders.v1',
        'esi-characters.read_corporation_roles.v1',
        'esi-location.read_online.v1'
    ]

    EVE_ALT_TYPES = (
        ("super_alt", "Super Alt"),
        ("rorqual_alt", "Rorqual Alt"),
        ("cap_alt", "Capital Alt"),
        ("subcap_pve_alt", "Subcap PvE Alt"),
        ("subcap_pvp_alt", "Subcap PvP Alt"),
        ("industry_alt", "Industry Alt"),
        ("useless_alt", "Useless Alt")
    )

    EVE_FLEET_TYPES = (
        ("cta", "Call to Arms"),
        ("mining", "Mining"),
        ("roam", "Roam"),
        ("other", "Other")
    )

    EVE_FLEET_VALUES = {
        "mining": 0.0,
        "roam": 0.0,
        "other": 0.0,
        "cta": 0.0
    }

    def ready(self):
        from django.contrib.auth.models import Group
        self.ESI_SECURITY = EsiSecurity(
            redirect_uri=self.ESI_CALLBACK_URL,
            client_id=self.ESI_CLIENT_ID,
            secret_key=self.ESI_SECRET_KEY,
            headers={'User-Agent': 'Krypted Development 3.0'}
        )
        self.ESI_CLIENT = EsiClient(
            security=self.ESI_SECURITY,
            cache=None,
            headers={'User-Agent': 'Krypted Development 3.0'}
        )
        self.ESI_URL_CACHE = self.ESI_SECURITY.get_auth_uri(scopes=self.ESI_SCOPES, state="jaiodfjasd8234has")