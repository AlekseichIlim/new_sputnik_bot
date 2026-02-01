from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, MetaData, Table, UniqueConstraint, Boolean, SmallInteger, \
    Date, Float, Boolean
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Brigade(Base):
    __tablename__ = 'brigades'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(25), unique=True, nullable=True)
    pl = Column(SmallInteger, nullable=True)
    processor = Column(Boolean, default=True)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(Integer, unique=True, nullable=True)
    name = Column(String(30), nullable=True)
    surname = Column(String(40), nullable=True)
    patronymic = Column(String(40), nullable=True)
    tab_number = Column(Integer, unique=True, nullable=False)
    post = Column(String(40), nullable=True)
    brigade = Column(Integer, ForeignKey('brigades.id'), nullable=True)


class Operator(Base):
    __tablename__ = 'operators'

    id = Column(Integer, primary_key=True, autoincrement=True)
    brigade = Column(Integer, ForeignKey('brigades.id', ondelete="CASCADE"), nullable=True)
    pl = Column(SmallInteger, nullable=True)
    date_shift = Column(Date)
    index_shift = Column(String(15), nullable=True)
    month = Column(SmallInteger, nullable=True)
    index_machine = Column(String(20), nullable=True)
    name = Column(String(50), nullable=True)
    eff_time = Column(Float, nullable=True)
    volume = Column(SmallInteger, nullable=True)
    UniqueConstraint('brigade', 'date_shift', 'index_shift', 'month', 'index_machine', name='uniq_id')


class DataMonth(Base):
    __tablename__ = 'data_month'
    id = Column(Integer, primary_key=True, autoincrement=True)
    # month = Column(SmallInteger, nullable=True)
    brigade = Column(Integer, ForeignKey('brigades.id', ondelete="CASCADE"), nullable=True)
    volume_plan_begin = Column(SmallInteger, nullable=True)
    volume_plan_finish_valka = Column(SmallInteger, nullable=True)
    volume_plan_finish_trelevka = Column(SmallInteger, nullable=True)
    volume_plan_day = Column(SmallInteger, nullable=True)
    percentage_completion = Column(SmallInteger, nullable=True)
    coefficient = Column(Float, nullable=True)
    volume_class_1 = Column(SmallInteger, nullable=True)
    volume_class_2 = Column(SmallInteger, nullable=True)


# class Shift(Base):
#
#     __tablename__ = 'shifts'
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     brigade = Column(Integer, ForeignKey('brigades.id', ondelete="CASCADE"), nullable=True)
#     date = Column(Date)
#     index = Column(String(15), nullable=True)
#     month = Column(SmallInteger, nullable=True)
#
#     fulling_1 = Column(String(20), nullable=True)
#     operator_fulling_1 = Column(String(50), nullable=True)
#     eff_time_full_1 = Column(Float, nullable=True)
#     volume_full_1 = Column(SmallInteger, nullable=True)
#     fulling_2 = Column(String(20), nullable=True)
#     operator_fulling_2 = Column(String(50), nullable=True)
#     eff_time_full_2 = Column(Float, nullable=True)
#     volume_full_2 = Column(SmallInteger, nullable=True)
#     fulling_3 = Column(String(20), nullable=True)
#     operator_fulling_3 = Column(String(50), nullable=True)
#     eff_time_full_3 = Column(Float, nullable=True)
#     volume_full_3 = Column(SmallInteger, nullable=True)
#     fulling_4 = Column(String(20), nullable=True)
#     operator_fulling_4 = Column(String(50), nullable=True)
#     eff_time_full_4 = Column(Float, nullable=True)
#     volume_full_4 = Column(SmallInteger, nullable=True)
#     fulling_5 = Column(String(20), nullable=True)
#     operator_fulling_5 = Column(String(50), nullable=True)
#     eff_time_full_5 = Column(Float, nullable=True)
#     volume_full_5 = Column(SmallInteger, nullable=True)
#     fulling_6 = Column(String(20), nullable=True)
#     operator_fulling_6 = Column(String(50), nullable=True)
#     eff_time_full_6 = Column(Float, nullable=True)
#     volume_full_6 = Column(SmallInteger, nullable=True)
#
#     processor_1 = Column(String(20), nullable=True)
#     operator_proc_1 = Column(String(50), nullable=True)
#     eff_time_proc_1 = Column(SmallInteger, nullable=True)
#     volume_proc_1 = Column(SmallInteger, nullable=True)
#     processor_2 = Column(String(20), nullable=True)
#     operator_proc_2 = Column(String(50), nullable=True)
#     eff_time_proc_2 = Column(SmallInteger, nullable=True)
#     volume_proc_2 = Column(SmallInteger, nullable=True)
#     processor_3 = Column(String(20), nullable=True)
#     operator_proc_3 = Column(String(50), nullable=True)
#     eff_time_proc_3 = Column(SmallInteger, nullable=True)
#     volume_proc_3 = Column(SmallInteger, nullable=True)
#     processor_4 = Column(String(20), nullable=True)
#     operator_proc_4 = Column(String(50), nullable=True)
#     eff_time_proc_4 = Column(SmallInteger, nullable=True)
#     volume_proc_4 = Column(SmallInteger, nullable=True)
#     processor_5 = Column(String(20), nullable=True)
#     operator_proc_5 = Column(String(50), nullable=True)
#     eff_time_proc_5 = Column(SmallInteger, nullable=True)
#     volume_proc_5 = Column(SmallInteger, nullable=True)
#     processor_6 = Column(String(20), nullable=True)
#     operator_proc_6 = Column(String(50), nullable=True)
#     eff_time_proc_6 = Column(SmallInteger, nullable=True)
#     volume_proc_6 = Column(SmallInteger, nullable=True)
#     processor_7 = Column(String(20), nullable=True)
#     operator_proc_7 = Column(String(50), nullable=True)
#     eff_time_proc_7 = Column(SmallInteger, nullable=True)
#     volume_proc_7 = Column(SmallInteger, nullable=True)
#     processor_8 = Column(String(20), nullable=True)
#     operator_proc_8 = Column(String(50), nullable=True)
#     eff_time_proc_8 = Column(SmallInteger, nullable=True)
#     volume_proc_8 = Column(SmallInteger, nullable=True)
#     processor_9 = Column(String(20), nullable=True)
#     operator_proc_9 = Column(String(50), nullable=True)
#     eff_time_proc_9 = Column(SmallInteger, nullable=True)
#     volume_proc_9 = Column(SmallInteger, nullable=True)
#     processor_10 = Column(String(20), nullable=True)
#     operator_proc_10 = Column(String(50), nullable=True)
#     eff_time_proc_10 = Column(SmallInteger, nullable=True)
#     volume_proc_10 = Column(SmallInteger, nullable=True)
#
#     forwarder_1 = Column(String(20), nullable=True)
#     operator_forw_1 = Column(String(50), nullable=True)
#     eff_time_forw_1 = Column(SmallInteger, nullable=True)
#     volume_forw_1 = Column(SmallInteger, nullable=True)
#     forwarder_2 = Column(String(20), nullable=True)
#     operator_forw_2 = Column(String(50), nullable=True)
#     eff_time_forw_2 = Column(SmallInteger, nullable=True)
#     volume_forw_2 = Column(SmallInteger, nullable=True)
#     forwarder_3 = Column(String(20), nullable=True)
#     operator_forw_3 = Column(String(50), nullable=True)
#     eff_time_forw_3 = Column(SmallInteger, nullable=True)
#     volume_forw_3 = Column(SmallInteger, nullable=True)
#     forwarder_4 = Column(String(20), nullable=True)
#     operator_forw_4 = Column(String(50), nullable=True)
#     eff_time_forw_4 = Column(SmallInteger, nullable=True)
#     volume_forw_4 = Column(SmallInteger, nullable=True)
#     forwarder_5 = Column(String(20), nullable=True)
#     operator_forw_5 = Column(String(50), nullable=True)
#     eff_time_forw_5 = Column(SmallInteger, nullable=True)
#     volume_forw_5 = Column(SmallInteger, nullable=True)
#     forwarder_6 = Column(String(20), nullable=True)
#     operator_forw_6 = Column(String(50), nullable=True)
#     eff_time_forw_6 = Column(SmallInteger, nullable=True)
#     volume_forw_6 = Column(SmallInteger, nullable=True)
#     forwarder_7 = Column(String(20), nullable=True)
#     operator_forw_7 = Column(String(50), nullable=True)
#     eff_time_forw_7 = Column(SmallInteger, nullable=True)
#     volume_forw_7 = Column(SmallInteger, nullable=True)
#     forwarder_8 = Column(String(20), nullable=True)
#     operator_forw_8 = Column(String(50), nullable=True)
#     eff_time_forw_8 = Column(SmallInteger, nullable=True)
#     volume_forw_8 = Column(SmallInteger, nullable=True)
#     forwarder_9 = Column(String(20), nullable=True)
#     operator_forw_9 = Column(String(50), nullable=True)
#     eff_time_forw_9 = Column(SmallInteger, nullable=True)
#     volume_forw_9 = Column(SmallInteger, nullable=True)
#     forwarder_10 = Column(String(20), nullable=True)
#     operator_forw_10 = Column(String(50), nullable=True)
#     eff_time_forw_10 = Column(SmallInteger, nullable=True)
#     volume_forw_10 = Column(SmallInteger, nullable=True)
#     forwarder_11 = Column(String(20), nullable=True)
#     operator_forw_11 = Column(String(50), nullable=True)
#     eff_time_forw_11 = Column(SmallInteger, nullable=True)
#     volume_forw_11 = Column(SmallInteger, nullable=True)
#     forwarder_12 = Column(String(20), nullable=True)
#     operator_forw_12 = Column(String(50), nullable=True)
#     eff_time_forw_12 = Column(SmallInteger, nullable=True)
#     volume_forw_12 = Column(SmallInteger, nullable=True)







