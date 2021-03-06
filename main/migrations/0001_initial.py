# Generated by Django 4.0.4 on 2022-05-21 11:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TblCategory',
            fields=[
                ('cat_id', models.AutoField(primary_key=True, serialize=False)),
                ('cat_name', models.CharField(db_collation='utf8_unicode_ci', max_length=100)),
                ('cat_image', models.TextField(db_collation='utf8_unicode_ci')),
                ('cat_type', models.IntegerField()),
                ('cat_status', models.IntegerField()),
            ],
            options={
                'db_table': 'tbl_category',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TblComment',
            fields=[
                ('cmt_id', models.AutoField(primary_key=True, serialize=False)),
                ('cmt_time', models.DateTimeField()),
                ('cmt_text', models.TextField()),
            ],
            options={
                'db_table': 'tbl_comment',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TblReport',
            fields=[
                ('report_id', models.AutoField(primary_key=True, serialize=False)),
                ('report_content', models.TextField()),
                ('report_status', models.IntegerField()),
            ],
            options={
                'db_table': 'tbl_report',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TblUsers',
            fields=[
                ('uid', models.CharField(db_collation='utf8_unicode_ci', max_length=100, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'tbl_users',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TblVideo',
            fields=[
                ('vid_id', models.AutoField(primary_key=True, serialize=False)),
                ('vid_title', models.CharField(db_collation='utf8_unicode_ci', max_length=500)),
                ('vid_url', models.TextField(db_collation='utf8_unicode_ci')),
                ('vid_thumbnail', models.TextField(db_collation='utf8_unicode_ci')),
                ('vid_description', models.TextField(db_collation='utf8_unicode_ci')),
                ('vid_view', models.IntegerField()),
                ('vid_duration', models.IntegerField()),
                ('vid_time', models.DateTimeField()),
                ('vid_avg_rate', models.FloatField()),
                ('vid_status', models.IntegerField()),
                ('vid_type', models.IntegerField()),
                ('vid_is_premium', models.IntegerField()),
            ],
            options={
                'db_table': 'tbl_video',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TblFav',
            fields=[
                ('vid', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='main.tblvideo')),
                ('is_fav', models.IntegerField()),
            ],
            options={
                'db_table': 'tbl_fav',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TblRating',
            fields=[
                ('vid', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='main.tblvideo')),
                ('rate_score', models.IntegerField()),
                ('rate_status', models.IntegerField()),
            ],
            options={
                'db_table': 'tbl_rating',
                'managed': False,
            },
        ),
    ]
