from .repos import member_repo

class MemberService(object):

    def get_by_line_id(self, line_id):
        member = member_repo.get_by_line_id(line_id)
        if not member:
            return

        member.save()


member_service = MemberService()