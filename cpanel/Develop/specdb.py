# PhysicianSpecialization
specialization = models.ForeignKey(Specialization, models.DO_NOTHING, db_column='Specialization_ID')


def get_value(self):
    return self.specialization.name

# Physician


@property
def get_Specialization(self):
    physician = get_object_or_none(Physician, physician_nn=self.physician_nn)
    return PhysicianSpecialization.objects.filter(physician_nn=physician)
