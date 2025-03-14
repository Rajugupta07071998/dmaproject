from django.db import models
import uuid
from account.models import User

# Create your models here.

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True



class PersonalInfo(BaseModel):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='PersonalInfo/profile_pics/', null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.get_full_name()} - Personal Info'



class BusinessInfo(BaseModel):
    BUSINESS_TYPE_CHOICES = (
        ('music_academy', 'Music Academy'),
        ('dance_academy', 'Dance Academy'),
        ('art_academy', 'Art Academy'),
        ('sports_academy', 'Sports Academy'),
        ('coaching_center', 'Coaching Center'),
        ('fitness_center', 'Gym & Fitness Center'),
        ('retail', 'Retail'),
        ('ecommerce', 'E-commerce'),
        ('technology', 'Technology'),
        ('finance', 'Finance'),
        ('education', 'Education'),
        ('healthcare', 'Healthcare'),
        ('hospitality', 'Hospitality'),
        ('manufacturing', 'Manufacturing'),
        ('services', 'Services'),
        ('real_estate', 'Real Estate'),
        ('other', 'Other'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business_type = models.CharField(max_length=30, choices=BUSINESS_TYPE_CHOICES, null=True, blank=True)
    business_owner = models.CharField(max_length=100, blank=True)
    business_name = models.CharField(max_length=255, blank=True)
    business_about = models.TextField(null=True, blank=True, help_text="Short description about the business")
    business_address = models.TextField()
    business_phone = models.CharField(max_length=15)
    business_website = models.URLField(null=True, blank=True)
    business_email = models.EmailField(null=True, blank=True)
    established_year = models.PositiveIntegerField(null=True, blank=True, help_text="Year of establishment")
    number_of_employees = models.PositiveIntegerField(null=True, blank=True)
    business_logo = models.ImageField(upload_to='BusinessInfo/business_logos/', null=True, blank=True)

    def __str__(self):
        return f'{self.user.get_full_name()} - {self.business_name}'



########################################### REQUESTS #############################################
class BusinessMembership(BaseModel):  # second create from business account
    business = models.ForeignKey(BusinessInfo, on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="business_memberships")
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} -> {self.business.business_name}"
    


class MembershipRequest(BaseModel):  # First create request from user
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )

    business = models.ForeignKey(BusinessInfo, on_delete=models.CASCADE, related_name="membership_requests")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="membership_requests")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def accept(self):
        """Accept request and add user to BusinessMembership"""
        if self.status == 'pending':
            self.status = 'accepted'
            self.save()
            BusinessMembership.objects.create(user=self.user, business=self.business)

    def reject(self):
        """Reject request"""
        if self.status == 'pending':
            self.status = 'rejected'
            self.save()

    def __str__(self):
        return f"{self.user.get_full_name()} -> {self.business.business_name} ({self.get_status_display()})"
    
    

class Achievement(BaseModel):
    business = models.ForeignKey(BusinessInfo, related_name='achievements', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    date_awarded = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='Achievement/images/', null=True, blank=True)
    achievement_link = models.URLField(max_length=500, null=True, blank=True)  


    def __str__(self):
        return f'{self.business.business_name} - {self.title}'
    


from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

class Notification(BaseModel):
    NOTIFICATION_TYPES = (
        ('join_request', 'Join Request'),
        ('request_accepted', 'Request Accepted'),
        ('request_rejected', 'Request Rejected'),
        ('post_like', 'Post Like'),
        ('post_comment', 'Post Comment'),
        ('other', 'Other'),
    )

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="sent_notifications")
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    
    # Generic ForeignKey for any model
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    object_id = models.CharField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"{self.recipient} - {self.notification_type} - {self.message[:30]}"

    class Meta:
        ordering = ['-created_at']



def create_feed_notification(user, instance, notification_type, message):
    Notification.objects.create(
        recipient=instance.user,  # Ensure `Post` model has `user`
        sender=user,  # Changed `actor` to `sender`
        notification_type=notification_type,  # Changed `verb` to `notification_type`
        message=message,  # Added a meaningful message  
        content_type=ContentType.objects.get_for_model(instance.__class__),  # Post model
        object_id=instance.id
    )


def create_comment_notification(user, story):
    Notification.objects.create(
        recipient=story.user,  # Ensure `Story` model has `user`
        sender=user,  # Changed `actor` to `sender`
        notification_type='post_comment',  # Changed `verb` to `notification_type`
        message=f"{user.username} commented on your story.",  # Added a meaningful message
        content_type=ContentType.objects.get_for_model(story.__class__),  # Story model
        object_id=story.id
    )




class EquipmentMaster(BaseModel):
    """
    Model to store equipment details.
    
    Attributes:
        - `name` (CharField): Name of the equipment.
        - `description` (TextField): Description of the equipment.
        - `no_of_equipment` (IntegerField): Total number of equipment available.
        - `is_system` (BooleanField): Indicates if the equipment is a system-related item.
        - `image` (ImageField): Equipment image.
    """
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    no_of_equipment = models.IntegerField(default=0)
    is_system = models.BooleanField(default=False)  
    image = models.ImageField(upload_to="EquipmentMaster/equipment_images/", blank=True, null=True)

    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="equipment_master", blank=True, null=True
    )  

    def __str__(self):
        return self.name
