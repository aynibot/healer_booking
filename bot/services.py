from .repos import member_repo

class MemberService(object):

    def get_by_line_id(self, line_id):
        member = member_repo.get_by_line_id(line_id)
        if not member:
            return

        member.save()
        return member

    def get_by_member_ids(self, member_ids):
        return member_repo.get_by_ids(member_ids)

    def get_admins(self):
        return member_repo.get_admins()

member_service = MemberService()