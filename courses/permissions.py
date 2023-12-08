from rest_framework.permissions import BasePermission


class IsNotModerator(BasePermission):
    def has_permission(self, request, view):
        return not request.user.groups.filter(name='moderators')


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner
