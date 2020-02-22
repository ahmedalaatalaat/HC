# PhysicianSpecialization
specialization = models.ForeignKey(Specialization, models.DO_NOTHING, db_column='Specialization_ID')


def get_value(self):
    return self.specialization.name

# Physician


@property
def get_Specialization(self):
    return PhysicianSpecialization.objects.filter(physician_nn=self)
