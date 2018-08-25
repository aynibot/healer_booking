from .models import Member
from .utils import get_bot_api


class MemberRepo(object):
    def get_by_line_id(self, line_id):
        member, created = Member.objects.get_or_create(line_id=line_id)
        if created:
            line_bot_api = get_bot_api()
            profile = line_bot_api.get_profile(line_id)
            member.name = profile.display_name
            member.photo = profile.picture_url
            member.save()

        return member



member_repo = MemberRepo()