from django.db import migrations, models
import uuid

def generate_references(apps, schema_editor):
    Reservation = apps.get_model('jo_app', 'Reservation')
    for reservation in Reservation.objects.all():
        reservation.reference = str(uuid.uuid4())
        reservation.save()

class Migration(migrations.Migration):

    dependencies = [
        ('jo_app', '0002_offre_prix'),  # modifie selon ta dernière migration
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='reference',
            field=models.CharField(max_length=100, unique=True, null=True),
        ),
        migrations.RunPython(generate_references),
        migrations.AlterField(
            model_name='reservation',
            name='reference',
            field=models.CharField(max_length=100, unique=True, null=False),
        ),
    ]
