from rest_framework import permissions

from .models import *


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method == 'POST':

            if 'post_id' in request.data:
                pk = request.data['post_id']
                p = Post.objects.get(pk=pk)
                return p.person == request.user
        return True
