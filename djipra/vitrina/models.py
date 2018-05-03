from django.db import models
from django.core.exceptions import ValidationError

SEX_CHOISES = (
    (1, 'М'),
    (2, 'Ж'),
)

PRG_CHOISES = (
    (1, 'ИПР'),
    (2, 'ПРП'),
)


class AppVer(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)
    vers = models.CharField(max_length=5, blank=True, null=True)
    udt = models.DateTimeField()
    adt = models.DateTimeField()

    def __str__(self):
        return '{name} / {vers}'.format(name=self.name, vers=self.vers)

    class Meta:
        managed = False
        db_table = 'app_ver'
        verbose_name = 'Контроль версий'
        verbose_name_plural = 'Контроль версий'


class DelLog(models.Model):
    t_name = models.TextField()  # This field type is a guess.
    t_id = models.IntegerField()
    udt = models.DateTimeField()
    adt = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'del_log'
        verbose_name = 'Удаленные записи'
        verbose_name_plural = 'Удаленные записи'


class Prg(models.Model):
    okr = models.ForeignKey('PrgOkr', models.DO_NOTHING, blank=False, null=False, verbose_name='Код округа',
                            default=9)
    nreg = models.ForeignKey('PrgReg', models.DO_NOTHING, db_column='nreg', blank=False, null=False,
                             verbose_name='Код региона', default=92)
    dt = models.DateField(blank=True, null=True, verbose_name='Дата разработки')
    snils = models.CharField(max_length=15, blank=False, null=False, verbose_name='СНИЛС')
    lname = models.CharField(max_length=30, blank=True, null=True, verbose_name='Фамилия')
    fname = models.CharField(max_length=30, blank=True, null=True, verbose_name='Имя')
    sname = models.CharField(max_length=30, blank=True, null=True, verbose_name='Отчество')
    bdate = models.DateField(blank=True, null=True, verbose_name='Дата рождения')
    gndr = models.SmallIntegerField(blank=True, null=True, choices=SEX_CHOISES, verbose_name='Пол')
    oivid = models.ForeignKey('PrgOiv', models.DO_NOTHING, db_column='oivid', blank=True, null=True,
                              verbose_name='Орган исполнительной власти')
    docnum = models.CharField(max_length=30, blank=True, null=True, verbose_name='Номер документа')
    docdt = models.DateField(blank=True, null=True, verbose_name='Дата выдачи')
    prg = models.SmallIntegerField(blank=True, null=True, choices=PRG_CHOISES, verbose_name='Программа: 1-ИПР, 2-ПРП')
    prgnum = models.CharField(max_length=30, blank=True, null=True, verbose_name='Номер ИПР/ПРП')
    prgdt = models.DateField(blank=True, null=True, verbose_name='Дата выдачи ИПР')
    mseid = models.CharField(max_length=36, blank=False, null=False, verbose_name='Ключ ИПР/ПРП из ФБ МСЭ')
    udt = models.DateTimeField(verbose_name='', editable=False)
    adt = models.DateTimeField(verbose_name='', editable=False, auto_now_add=True)

    def clean(self):
        if self.snils is None:
            raise ValidationError('СНИЛС не заполнен')

        sn = ''.join(filter(lambda x: x.isdigit(), self.snils))
        print(sn)
        if len(sn) != 11:
            raise ValidationError('В СНИЛСе 11 цифр')

        def snils_csum(snils):
            k = range(9, 0, -1)
            pairs = zip(k, [int(x) for x in snils[:-2]])
            return sum([k * v for k, v in pairs])

        csum = snils_csum(sn)

        while csum > 101:
            csum %= 101
        if csum in (100, 101):
            csum = 0

        if csum != int(sn[-2:]):
            raise ValidationError('Контрольная сумма СНИЛС не сходится')

    class Meta:
        managed = False
        db_table = 'prg'
        verbose_name = 'Список ИПР и ПРП'
        verbose_name_plural = 'Список ИПР и ПРП'

    def __str__(self):
        return '{lname} {fname}  {mname}'.format(lname=self.lname, mname=self.sname, fname=self.fname)


class PrgOiv(models.Model):
    name = models.CharField(max_length=1024, blank=True, null=True)
    shname = models.CharField(max_length=64, blank=True, null=True)
    arc = models.DateField(blank=True, null=True)
    udt = models.DateTimeField()
    adt = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'prg_oiv'
        verbose_name = 'орган исполнительной власти'
        verbose_name_plural = 'органы исполнительной власти'


class PrgOkr(models.Model):
    name = models.CharField(max_length=1024, blank=True, null=True)
    shname = models.CharField(max_length=64, blank=True, null=True)
    arc = models.DateField(blank=True, null=True)
    udt = models.DateTimeField()
    adt = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'prg_okr'
        verbose_name = 'Округ'
        verbose_name_plural = 'Округ'
        ordering = ['name']


class PrgReg(models.Model):
    okr = models.ForeignKey(PrgOkr, models.DO_NOTHING)
    name = models.CharField(max_length=1024, blank=True, null=True)
    shname = models.CharField(max_length=64, blank=True, null=True)
    arc = models.DateField(blank=True, null=True)
    udt = models.DateTimeField()
    adt = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'prg_reg'
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'
        ordering = ['name']


class PrgRhb(models.Model):
    prgid = models.ForeignKey(Prg, models.DO_NOTHING, db_column='prgid')
    typeid = models.ForeignKey('RhbType', models.DO_NOTHING, db_column='typeid')
    evntid = models.ForeignKey('RhbEvnt', models.DO_NOTHING, db_column='evntid', blank=True, null=True)
    dicid = models.ForeignKey('RhbDic', models.DO_NOTHING, db_column='dicid', blank=True, null=True)
    tsrid = models.ForeignKey('RhbTsr', models.DO_NOTHING, db_column='tsrid', blank=True, null=True)
    name = models.CharField(max_length=128, blank=True, null=True)
    dt_exc = models.DateField(blank=True, null=True)
    excid = models.ForeignKey('RhbExc', models.DO_NOTHING, db_column='excid', blank=True, null=True)
    execut = models.CharField(max_length=128, blank=True, null=True)
    resid = models.ForeignKey('RhbRes', models.DO_NOTHING, db_column='resid', blank=True, null=True)
    par1 = models.IntegerField(blank=True, null=True)
    par2 = models.IntegerField(blank=True, null=True)
    par3 = models.IntegerField(blank=True, null=True)
    result = models.CharField(max_length=128, blank=True, null=True)
    note = models.CharField(max_length=256, blank=True, null=True)
    udt = models.DateTimeField()
    adt = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'prg_rhb'
        verbose_name = 'ИПР/ПРП - реабилитация'
        verbose_name_plural = 'ИПР/ПРП - реабилитация'
        ordering = ['name']



class RhbDic(models.Model):
    name = models.CharField(max_length=1024, blank=True, null=True)
    shname = models.CharField(max_length=64, blank=True, null=True)
    arc = models.DateField(blank=True, null=True)
    udt = models.DateTimeField()
    adt = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'rhb_dic'
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'
        ordering = ['name']


class RhbEvnt(models.Model):
    typeid = models.ForeignKey('RhbType', models.DO_NOTHING, db_column='typeid')
    name = models.CharField(max_length=1024, blank=True, null=True)
    shname = models.CharField(max_length=64, blank=True, null=True)
    arc = models.DateField(blank=True, null=True)
    udt = models.DateTimeField()
    adt = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'rhb_evnt'
        verbose_name = 'Подтип мероприятия'
        verbose_name_plural = 'Подтипы мероприятий'
        ordering = ['name']


class RhbExc(models.Model):
    name = models.CharField(max_length=1024, blank=True, null=True)
    scode = models.CharField(max_length=64, blank=True, null=True)
    inn = models.CharField(max_length=12, blank=True, null=True)
    ogrn = models.CharField(max_length=15, blank=True, null=True)
    arc = models.DateField(blank=True, null=True)
    udt = models.DateTimeField()
    adt = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'rhb_exc'
        verbose_name = 'Организации исполнители мероприятий'
        verbose_name_plural = 'Организации исполнители мероприятий'
        ordering = ['name']


class RhbGrp(models.Model):
    name = models.CharField(max_length=1024, blank=True, null=True)
    shname = models.CharField(max_length=64, blank=True, null=True)
    arc = models.DateField(blank=True, null=True)
    udt = models.DateTimeField()
    adt = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'rhb_grp'
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'
        ordering = ['name']


class RhbGtsr(models.Model):
    name = models.CharField(max_length=1024, blank=True, null=True)
    scode = models.CharField(max_length=20, blank=True, null=True)
    arc = models.DateField(blank=True, null=True)
    udt = models.DateTimeField()

    def __str__(self):
        return self.name

    adt = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'rhb_gtsr'
        verbose_name = 'Группа ТСР'
        verbose_name_plural = 'Группы ТСР'
        ordering = ['name']


class RhbRes(models.Model):
    name = models.CharField(max_length=1024, blank=True, null=True)
    shname = models.CharField(max_length=64, blank=True, null=True)
    arc = models.DateField(blank=True, null=True)
    udt = models.DateTimeField()
    adt = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'rhb_res'
        verbose_name = 'Результат выполнения мероприятия'
        verbose_name_plural = 'Результаты выполнения мероприятия'
        ordering = ['name']


class RhbTsr(models.Model):
    gtsrid = models.ForeignKey(RhbGtsr, models.DO_NOTHING, db_column='gtsrid')
    name = models.CharField(max_length=1024, blank=True, null=True)
    scode = models.CharField(max_length=20, blank=True, null=True)
    p374n = models.CharField(max_length=20, blank=True, null=True)
    arc = models.DateField(blank=True, null=True)
    udt = models.DateTimeField()
    adt = models.DateTimeField()

    def __str__(self):
        return self.name[:100]

    class Meta:
        managed = False
        db_table = 'rhb_tsr'
        verbose_name = 'ТСР'
        verbose_name_plural = 'Справочник ТСР'
        ordering = ['name']


class RhbType(models.Model):
    grpid = models.ForeignKey(RhbGrp, models.DO_NOTHING, db_column='grpid')
    name = models.CharField(max_length=1024, blank=True, null=True)
    shname = models.CharField(max_length=64, blank=True, null=True)
    arc = models.DateField(blank=True, null=True)
    udt = models.DateTimeField()
    adt = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'rhb_type'
        verbose_name = 'Тип мероприятий'
        verbose_name_plural = 'Типы мероприятий'
        ordering = ['name']
