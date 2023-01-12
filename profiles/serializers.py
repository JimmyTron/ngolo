from rest_framework import serializers
from django.db import transaction

from profiles.models import User, Profile

"""Serializer to display Profile details to be used in the UserSerializer"""
class ProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'profile_name', 'bio']


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    number_of_profiles = serializers.IntegerField(read_only=True) #Added field to display the number of profiles that a user has.
    profile = ProfileDetailSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'phone_number', 'password', 'number_of_profiles', 'profile']

"""Serializer to display the User Details to be used on profile registration"""
class UserDetailsSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'password']


"""
Serializer for registration of user and first profile that is created when a user is registered
It ensures that a first user does not exist without an profile.
"""
class UserProfileRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={"input_type": "password"}, write_only=True)
    user = UserDetailsSerializer()

    def create(self, validated_data):
        user = dict(self.validated_data['user'])
        password = user['password']
        confirm_password = self.validated_data['confirm_password']

        if password == confirm_password:
            with transaction.atomic():
                user = User.objects.create_user(username=user['username'], first_name=user['first_name'], last_name=user['last_name'], email=user['email'], phone_number=user['phone_number'], password=password)

                profile = Profile.objects.create(user=user, profile_name=self.validated_data['profile_name'], bio=self.validated_data['bio'])

                return profile
                
    class Meta:
        model = Profile
        fields = ['id', 'user', 'confirm_password', 'profile_name', 'display_picture', 'bio']


"""Serializer that enables addition of a new profile to an existing user"""
class AddProfileSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user_id = self.context['user_id']
        profile_name = self.validated_data['profile_name']
        bio = self.validated_data['bio']

        user = User.objects.get(pk=user_id)

        profile = Profile.objects.create(user=user, profile_name=profile_name, bio=bio)

        return profile
    class Meta:
        model = Profile
        fields = ['id','profile_name', 'bio']
