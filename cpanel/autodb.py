from django.contrib.auth.models import Group
from .models import Specialization
from django.http import HttpResponse


def group_add(request):
    # --Stakeholder
    Group.objects.create(
        name='Stakeholder'
    )
    Group.objects.create(
        name='Physician'
    )
    Group.objects.create(
        name='Patient'
    )
    Group.objects.create(
        name='Nurse'
    )
    Group.objects.create(
        name='Paramedic'
    )
    Group.objects.create(
        name='Specialist'
    )
    Group.objects.create(
        name='Pharmacist'
    )
    # --Medical Institution
    Group.objects.create(
        name='Medical Institution'
    )
    Group.objects.create(
        name='Lab'
    )
    Group.objects.create(
        name='Clinic'
    )
    Group.objects.create(
        name='Hospital'
    )
    Group.objects.create(
        name='Pharmacy'
    )
    # --Insurance Company
    Group.objects.create(
        name='Insurance Company'
    )
    return HttpResponse("<h1>New groups has been added</h1>")


def specialization_add(request):
    Specialization.objects.create(
        specialization_id=1,
        name='Dermatology (Skin)',
    )
    Specialization.objects.create(
        specialization_id=2,
        name='Dentistry (Teeth)',
    )
    Specialization.objects.create(
        specialization_id=3,
        name='Psychiatry (Mental, Emotional or Behavioral Disorders)',
    )
    Specialization.objects.create(
        specialization_id=4,
        name='Pediatrics and New Born (Child)',
    )
    Specialization.objects.create(
        specialization_id=5,
        name='Neurology (Brain & Nerves)',
    )
    Specialization.objects.create(
        specialization_id=6,
        name='Orthopedics (Bones)',
    )
    Specialization.objects.create(
        specialization_id=7,
        name='Gynaecology and Infertility',
    )
    Specialization.objects.create(
        specialization_id=8,
        name='Ear, Nose and Throat',
    )
    Specialization.objects.create(
        specialization_id=9,
        name='Cardiology and Vascular Disease (Heart)',
    )
    Specialization.objects.create(
        specialization_id=10,
        name='Allergy and Immunology (Sensitivity and Immunity)',
    )
    Specialization.objects.create(
        specialization_id=11,
        name='Andrology and Male Infertility',
    )
    Specialization.objects.create(
        specialization_id=12,
        name='Audiology, Cardiology and Thoracic Surgery (Heart & Chest)',
    )
    Specialization.objects.create(
        specialization_id=13,
        name='Chest and Respiratory',
    )
    Specialization.objects.create(
        specialization_id=14,
        name='Diabetes and Endocrinology',
    )
    Specialization.objects.create(
        specialization_id=15,
        name='Diagnostic Radiology (Scan Centers)',
    )
    Specialization.objects.create(
        specialization_id=16,
        name='Family Medicine',
    )
    Specialization.objects.create(
        specialization_id=17,
        name='Gastroenterology and Endoscopy',
    )
    Specialization.objects.create(
        specialization_id=18,
        name='General Practice',
    )
    Specialization.objects.create(
        specialization_id=19,
        name='General Surgery',
    )
    Specialization.objects.create(
        specialization_id=20,
        name='Geriatrics (Old People Health)',
    )
    Specialization.objects.create(
        specialization_id=21,
        name='Hematology, Hepatology (Liver Doctor)',
    )
    Specialization.objects.create(
        specialization_id=22,
        name='Internal Medicin',
    )
    Specialization.objects.create(
        specialization_id=23,
        name='IVF and Infertility',
    )
    Specialization.objects.create(
        specialization_id=24,
        name='Laboratories',
    )
    Specialization.objects.create(
        specialization_id=25,
        name='Nephrology',
    )
    Specialization.objects.create(
        specialization_id=26,
        name='Neurosurgery (Brain & Nerves Surgery)',
    )
    Specialization.objects.create(
        specialization_id=27,
        name='Obesity and Laparoscopic Surgery',
    )
    Specialization.objects.create(
        specialization_id=28,
        name='Oncology (Tumor)',
    )
    Specialization.objects.create(
        specialization_id=29,
        name='Oncology Surgery (Tumor Surgery)',
    )
    Specialization.objects.create(
        specialization_id=30,
        name='Ophthalmology (Eyes)',
    )
    Specialization.objects.create(
        specialization_id=31,
        name='Osteopathy (Osteopathic Medicine)',
    )
    Specialization.objects.create(
        specialization_id=32,
        name='Pain Management',
    )
    Specialization.objects.create(
        specialization_id=33,
        name='Pediatric Surgery',
    )
    Specialization.objects.create(
        specialization_id=34,
        name='Phoniatrics (Speech)',
    )
    Specialization.objects.create(
        specialization_id=35,
        name='Physiotherapy and Sport Injuries',
    )
    Specialization.objects.create(
        specialization_id=36,
        name='Plastic Surgery',
    )
    Specialization.objects.create(
        specialization_id=37,
        name='Rheumatology',
    )
    Specialization.objects.create(
        specialization_id=38,
        name='Spinal Surgery',
    )
    Specialization.objects.create(
        specialization_id=39,
        name='Urology (Urinary System)',
    )
    Specialization.objects.create(
        specialization_id=40,
        name='Vascular Surgery (Arteries and Vein Surgery)',
    )
    return HttpResponse("<h1>New specializations has been added</h1>")
