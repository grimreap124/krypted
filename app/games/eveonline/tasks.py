from __future__ import absolute_import, unicode_literals
from celery import task
from games.eveonline.models import Token, EveCharacter
from django.contrib.auth.models import User, Group
from core.models import Profile, Guild
from esipy import App, EsiClient, EsiSecurity
from django.conf import settings
import logging, time

logger = logging.getLogger(__name__)

"""
MAJOR TASKS
These tasks are periodically ran.
"""
@task()
def verify_sso_tokens():
    logger.info("Verifying all SSO tokens")
    tokens = Token.objects.all()
    for token in tokens:
        verify_sso_token.apply_async(args=[token.character_id])


@task()
def sync_users():
    logger.info("Bulk updating all users for EVE Online roles")
    call_count = 0
    for user in User.objects.filter(groups__name=settings.EVE_ONLINE_GROUP):
        logger.info("Syncing EVE Online permissions for %s" % user.username)
        if Token.objects.filter(user=user).count() > 0:
            sync_user.apply_async(args=[user.pk], countdown=call_count*10)
            call_count += 1
        else:
            try:
                Profile.objects.get(user=user).guilds.remove(Guild.objects.get(group__name=settings.EVE_ONLINE_GROUP))
            except:
                pass
            user.groups.remove(Group.objects.get(name=settings.EVE_ONLINE_GROUP))
            user.groups.add(Group.objects.get(name=settings.GUEST_GROUP))



"""
MINOR TASKS
These tasks build the above tasks.
"""
@task()
def verify_sso_token(character_id):
    token = Token.objects.get(character_id=character_id)
    character = EveCharacter.objects.get(token=token)
    settings.ESI_SECURITY.update_token(token.populate())
    logger.info("Syncing token for %s" % character.character_name)
    try:
        settings.ESI_SECURITY.refresh()
        character.update_corporation()
        sync_user.apply_async(args=[token.user.pk], countdown=10)
    except Exception as e:
        logger.info("Token of %s expired for %s. %s" % (character, token.user, e))
        character.character_corporation = "ERROR"
        character.character_alliance = "ERROR"
        character.save()
        sync_user.apply_async(args=[token.user.pk])

@task()
def sync_user(user):
    # Get user information
    user = User.objects.get(pk=user)
    logger.info("Syncing user %s for EVE Online..." % user.username)
    profile = Profile.objects.get(user=user)
    if not EveCharacter.objects.filter(main=None, user=user):
        if Group.objects.get(name=settings.EVE_ONLINE_MAIN_GROUP) in user.groups.all():
            user.groups.remove(Group.objects.get(name=settings.EVE_ONLINE_MAIN_GROUP))
        if Group.objects.get(name=settings.EVE_ONLINE_GROUP) in user.groups.all():
            user.groups.remove(Group.objects.get(name=settings.EVE_ONLINE_GROUP))
        user.groups.add(Group.objects.get(name=settings.GUEST_GROUP))
    else:
        main_character = EveCharacter.objects.get(main=None, user=user)
        main_status = False
        secondary_status = False
        if settings.ALLIANCE_MODE:
            if str(main_character.corporation.alliance_id) in settings.MAIN_ENTITY_ID:
                main_status = True
            elif str(main_character.corporation.alliance_id) in settings.SECONDARY_ENTITY_IDS:
                secondary_status = True
            else:
                if Group.objects.get(name=settings.EVE_ONLINE_GROUP) in user.groups.all():
                    user.groups.remove(Group.objects.get(name=settings.EVE_ONLINE_GROUP))
                user.groups.add(Group.objects.get(name=settings.GUEST_GROUP))
        else:
            if str(main_character.corporation.corporation_id) in settings.MAIN_ENTITY_ID:
                main_status = True
            elif str(main_character.corporation.corporation_id) in settings.SECONDARY_ENTITY_IDS:
                secondary_status = True
            else:
                if Group.objects.get(name=settings.EVE_ONLINE_GROUP) in user.groups.all():
                    user.groups.remove(Group.objects.get(name=settings.EVE_ONLINE_GROUP))
                user.groups.add(Group.objects.get(name=settings.GUEST_GROUP))

        if main_status:
                user.groups.add(Group.objects.get(name=settings.EVE_ONLINE_MAIN_GROUP))
                time.sleep(1)
                user.groups.add(Group.objects.get(name=settings.EVE_ONLINE_GROUP))
                time.sleep(1)
                user.groups.add(Group.objects.get(name=settings.RECRUIT_GROUP))
                if Group.objects.get(name=settings.GUEST_GROUP) in user.groups.all():
                    user.groups.remove(Group.objects.get(name=settings.GUEST_GROUP))
                profile.guilds.add(Guild.objects.get(group__name=settings.EVE_ONLINE_GROUP))

        if secondary_status:
                user.groups.add(Group.objects.get(name=settings.EVE_ONLINE_GROUP))
                time.sleep(1)
                user.groups.add(Group.objects.get(name=settings.RECRUIT_GROUP))
                if Group.objects.get(name=settings.GUEST_GROUP) in user.groups.all():
                    user.groups.remove(Group.objects.get(name=settings.GUEST_GROUP))
                profile.guilds.add(Guild.objects.get(group__name=settings.EVE_ONLINE_GROUP))
