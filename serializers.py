from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserPublicSerializer(serializers.ModelSerializer):
    """Serializer for public user info (channel page, video uploader)."""
    video_count = serializers.SerializerMethodField()
    total_views = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'channel_name', 'avatar', 'bio', 'video_count', 'total_views', 'created_at')

    def get_video_count(self, obj):
        return obj.videos.filter(is_published=True).count()

    def get_total_views(self, obj):
        from django.db.models import Sum
        return obj.videos.filter(is_published=True).aggregate(Sum('views'))['views__sum'] or 0

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for own profile management."""
    video_count = serializers.SerializerMethodField()
    total_views = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'channel_name', 'avatar', 'bio', 'video_count', 'total_views', 'created_at')
        read_only_fields = ('id', 'email', 'created_at')

    def get_video_count(self, obj):
        return obj.videos.count()

    def get_total_views(self, obj):
        from django.db.models import Sum
        return obj.videos.aggregate(Sum('views'))['views__sum'] or 0

class RegisterSerializer(serializers.ModelSerializer):
    """Handles new user registration."""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)
    channel_name = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'channel_name', 'password', 'password_confirm')

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        if not attrs.get('channel_name'):
            attrs['channel_name'] = attrs['username']

        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            channel_name=validated_data['channel_name'],
            password=validated_data['password']
        )
        return user
