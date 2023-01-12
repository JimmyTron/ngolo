from django.db.models import Count
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from profiles.models import *
from profiles.serializers import *
from profiles.models import *


"""Api View for listing all users and retrieving specific users using their id's"""
class UserViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        if self.request.method == 'GET':
            return User.objects.annotate(number_of_profiles=Count('profile'))#Adds a new column that counts the number of profiles.
        return User.objects.all()


"""Api view to be used when a user first registers to the system"""
class RegisterProfileViewSet(CreateModelMixin, GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = UserProfileRegistrationSerializer


"""Api view for a user to add another new profile"""
class AddUserProfileViewSet(ModelViewSet):
    serializer_class = AddProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'user_id': self.kwargs['user_pk']}

    def get_queryset(self):
        return Profile.objects.filter(user_id=self.kwargs['user_pk'])
