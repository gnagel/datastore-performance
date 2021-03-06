from __future__ import absolute_import

from google.appengine.ext import db
from google.appengine.ext import ndb

from datastore_performance import sql_api, ndb_api, db_api


#
# sql Models to test: 10x && 100x
#
# The `keys`, `get`, and `put` methods are provided by the helpers in `sql_api`.
#
class PgModel10(sql_api.PgQueryMixin, db.Model):
    prop_0 = db.StringProperty(indexed=False)
    prop_1 = db.StringProperty(indexed=False)
    prop_2 = db.StringProperty(indexed=False)
    prop_3 = db.StringProperty(indexed=False)
    prop_4 = db.StringProperty(indexed=False)
    prop_5 = db.StringProperty(indexed=False)
    prop_6 = db.StringProperty(indexed=False)
    prop_7 = db.StringProperty(indexed=False)
    prop_8 = db.StringProperty(indexed=False)
    prop_9 = db.StringProperty(indexed=False)


class PgModel100(PgModel10):
    prop_10 = db.StringProperty(indexed=False)
    prop_11 = db.StringProperty(indexed=False)
    prop_12 = db.StringProperty(indexed=False)
    prop_13 = db.StringProperty(indexed=False)
    prop_14 = db.StringProperty(indexed=False)
    prop_15 = db.StringProperty(indexed=False)
    prop_16 = db.StringProperty(indexed=False)
    prop_17 = db.StringProperty(indexed=False)
    prop_18 = db.StringProperty(indexed=False)
    prop_19 = db.StringProperty(indexed=False)
    prop_20 = db.StringProperty(indexed=False)
    prop_21 = db.StringProperty(indexed=False)
    prop_22 = db.StringProperty(indexed=False)
    prop_23 = db.StringProperty(indexed=False)
    prop_24 = db.StringProperty(indexed=False)
    prop_25 = db.StringProperty(indexed=False)
    prop_26 = db.StringProperty(indexed=False)
    prop_27 = db.StringProperty(indexed=False)
    prop_28 = db.StringProperty(indexed=False)
    prop_29 = db.StringProperty(indexed=False)
    prop_30 = db.StringProperty(indexed=False)
    prop_31 = db.StringProperty(indexed=False)
    prop_32 = db.StringProperty(indexed=False)
    prop_33 = db.StringProperty(indexed=False)
    prop_34 = db.StringProperty(indexed=False)
    prop_35 = db.StringProperty(indexed=False)
    prop_36 = db.StringProperty(indexed=False)
    prop_37 = db.StringProperty(indexed=False)
    prop_38 = db.StringProperty(indexed=False)
    prop_39 = db.StringProperty(indexed=False)
    prop_40 = db.StringProperty(indexed=False)
    prop_41 = db.StringProperty(indexed=False)
    prop_42 = db.StringProperty(indexed=False)
    prop_43 = db.StringProperty(indexed=False)
    prop_44 = db.StringProperty(indexed=False)
    prop_45 = db.StringProperty(indexed=False)
    prop_46 = db.StringProperty(indexed=False)
    prop_47 = db.StringProperty(indexed=False)
    prop_48 = db.StringProperty(indexed=False)
    prop_49 = db.StringProperty(indexed=False)
    prop_50 = db.StringProperty(indexed=False)
    prop_51 = db.StringProperty(indexed=False)
    prop_52 = db.StringProperty(indexed=False)
    prop_53 = db.StringProperty(indexed=False)
    prop_54 = db.StringProperty(indexed=False)
    prop_55 = db.StringProperty(indexed=False)
    prop_56 = db.StringProperty(indexed=False)
    prop_57 = db.StringProperty(indexed=False)
    prop_58 = db.StringProperty(indexed=False)
    prop_59 = db.StringProperty(indexed=False)
    prop_60 = db.StringProperty(indexed=False)
    prop_61 = db.StringProperty(indexed=False)
    prop_62 = db.StringProperty(indexed=False)
    prop_63 = db.StringProperty(indexed=False)
    prop_64 = db.StringProperty(indexed=False)
    prop_65 = db.StringProperty(indexed=False)
    prop_66 = db.StringProperty(indexed=False)
    prop_67 = db.StringProperty(indexed=False)
    prop_68 = db.StringProperty(indexed=False)
    prop_69 = db.StringProperty(indexed=False)
    prop_70 = db.StringProperty(indexed=False)
    prop_71 = db.StringProperty(indexed=False)
    prop_72 = db.StringProperty(indexed=False)
    prop_73 = db.StringProperty(indexed=False)
    prop_74 = db.StringProperty(indexed=False)
    prop_75 = db.StringProperty(indexed=False)
    prop_76 = db.StringProperty(indexed=False)
    prop_77 = db.StringProperty(indexed=False)
    prop_78 = db.StringProperty(indexed=False)
    prop_79 = db.StringProperty(indexed=False)
    prop_80 = db.StringProperty(indexed=False)
    prop_81 = db.StringProperty(indexed=False)
    prop_82 = db.StringProperty(indexed=False)
    prop_83 = db.StringProperty(indexed=False)
    prop_84 = db.StringProperty(indexed=False)
    prop_85 = db.StringProperty(indexed=False)
    prop_86 = db.StringProperty(indexed=False)
    prop_87 = db.StringProperty(indexed=False)
    prop_88 = db.StringProperty(indexed=False)
    prop_89 = db.StringProperty(indexed=False)
    prop_90 = db.StringProperty(indexed=False)
    prop_91 = db.StringProperty(indexed=False)
    prop_92 = db.StringProperty(indexed=False)
    prop_93 = db.StringProperty(indexed=False)
    prop_94 = db.StringProperty(indexed=False)
    prop_95 = db.StringProperty(indexed=False)
    prop_96 = db.StringProperty(indexed=False)
    prop_97 = db.StringProperty(indexed=False)
    prop_98 = db.StringProperty(indexed=False)
    prop_99 = db.StringProperty(indexed=False)


#
# db.Models to test: 10x && 100x
#
# The `keys` method is overridden here with the helpers in `db_api`.
#
class DbModel10(db_api.DbQueryMixin, db.Model):
    prop_0 = db.StringProperty(indexed=False)
    prop_1 = db.StringProperty(indexed=False)
    prop_2 = db.StringProperty(indexed=False)
    prop_3 = db.StringProperty(indexed=False)
    prop_4 = db.StringProperty(indexed=False)
    prop_5 = db.StringProperty(indexed=False)
    prop_6 = db.StringProperty(indexed=False)
    prop_7 = db.StringProperty(indexed=False)
    prop_8 = db.StringProperty(indexed=False)
    prop_9 = db.StringProperty(indexed=False)


class DbModel100(DbModel10):
    prop_10 = db.StringProperty(indexed=False)
    prop_11 = db.StringProperty(indexed=False)
    prop_12 = db.StringProperty(indexed=False)
    prop_13 = db.StringProperty(indexed=False)
    prop_14 = db.StringProperty(indexed=False)
    prop_15 = db.StringProperty(indexed=False)
    prop_16 = db.StringProperty(indexed=False)
    prop_17 = db.StringProperty(indexed=False)
    prop_18 = db.StringProperty(indexed=False)
    prop_19 = db.StringProperty(indexed=False)
    prop_20 = db.StringProperty(indexed=False)
    prop_21 = db.StringProperty(indexed=False)
    prop_22 = db.StringProperty(indexed=False)
    prop_23 = db.StringProperty(indexed=False)
    prop_24 = db.StringProperty(indexed=False)
    prop_25 = db.StringProperty(indexed=False)
    prop_26 = db.StringProperty(indexed=False)
    prop_27 = db.StringProperty(indexed=False)
    prop_28 = db.StringProperty(indexed=False)
    prop_29 = db.StringProperty(indexed=False)
    prop_30 = db.StringProperty(indexed=False)
    prop_31 = db.StringProperty(indexed=False)
    prop_32 = db.StringProperty(indexed=False)
    prop_33 = db.StringProperty(indexed=False)
    prop_34 = db.StringProperty(indexed=False)
    prop_35 = db.StringProperty(indexed=False)
    prop_36 = db.StringProperty(indexed=False)
    prop_37 = db.StringProperty(indexed=False)
    prop_38 = db.StringProperty(indexed=False)
    prop_39 = db.StringProperty(indexed=False)
    prop_40 = db.StringProperty(indexed=False)
    prop_41 = db.StringProperty(indexed=False)
    prop_42 = db.StringProperty(indexed=False)
    prop_43 = db.StringProperty(indexed=False)
    prop_44 = db.StringProperty(indexed=False)
    prop_45 = db.StringProperty(indexed=False)
    prop_46 = db.StringProperty(indexed=False)
    prop_47 = db.StringProperty(indexed=False)
    prop_48 = db.StringProperty(indexed=False)
    prop_49 = db.StringProperty(indexed=False)
    prop_50 = db.StringProperty(indexed=False)
    prop_51 = db.StringProperty(indexed=False)
    prop_52 = db.StringProperty(indexed=False)
    prop_53 = db.StringProperty(indexed=False)
    prop_54 = db.StringProperty(indexed=False)
    prop_55 = db.StringProperty(indexed=False)
    prop_56 = db.StringProperty(indexed=False)
    prop_57 = db.StringProperty(indexed=False)
    prop_58 = db.StringProperty(indexed=False)
    prop_59 = db.StringProperty(indexed=False)
    prop_60 = db.StringProperty(indexed=False)
    prop_61 = db.StringProperty(indexed=False)
    prop_62 = db.StringProperty(indexed=False)
    prop_63 = db.StringProperty(indexed=False)
    prop_64 = db.StringProperty(indexed=False)
    prop_65 = db.StringProperty(indexed=False)
    prop_66 = db.StringProperty(indexed=False)
    prop_67 = db.StringProperty(indexed=False)
    prop_68 = db.StringProperty(indexed=False)
    prop_69 = db.StringProperty(indexed=False)
    prop_70 = db.StringProperty(indexed=False)
    prop_71 = db.StringProperty(indexed=False)
    prop_72 = db.StringProperty(indexed=False)
    prop_73 = db.StringProperty(indexed=False)
    prop_74 = db.StringProperty(indexed=False)
    prop_75 = db.StringProperty(indexed=False)
    prop_76 = db.StringProperty(indexed=False)
    prop_77 = db.StringProperty(indexed=False)
    prop_78 = db.StringProperty(indexed=False)
    prop_79 = db.StringProperty(indexed=False)
    prop_80 = db.StringProperty(indexed=False)
    prop_81 = db.StringProperty(indexed=False)
    prop_82 = db.StringProperty(indexed=False)
    prop_83 = db.StringProperty(indexed=False)
    prop_84 = db.StringProperty(indexed=False)
    prop_85 = db.StringProperty(indexed=False)
    prop_86 = db.StringProperty(indexed=False)
    prop_87 = db.StringProperty(indexed=False)
    prop_88 = db.StringProperty(indexed=False)
    prop_89 = db.StringProperty(indexed=False)
    prop_90 = db.StringProperty(indexed=False)
    prop_91 = db.StringProperty(indexed=False)
    prop_92 = db.StringProperty(indexed=False)
    prop_93 = db.StringProperty(indexed=False)
    prop_94 = db.StringProperty(indexed=False)
    prop_95 = db.StringProperty(indexed=False)
    prop_96 = db.StringProperty(indexed=False)
    prop_97 = db.StringProperty(indexed=False)
    prop_98 = db.StringProperty(indexed=False)
    prop_99 = db.StringProperty(indexed=False)


#
# Expando Models to test: 10x && 100x
#
# The `keys` method is overridden here with the helpers in `db_api`.
#
class DbExpando10(db_api.DbQueryMixin, db.Expando):
    prop_0 = db.StringProperty(indexed=False)
    prop_1 = db.StringProperty(indexed=False)
    prop_2 = db.StringProperty(indexed=False)
    prop_3 = db.StringProperty(indexed=False)
    prop_4 = db.StringProperty(indexed=False)
    prop_5 = db.StringProperty(indexed=False)
    prop_6 = db.StringProperty(indexed=False)
    prop_7 = db.StringProperty(indexed=False)
    prop_8 = db.StringProperty(indexed=False)
    prop_9 = db.StringProperty(indexed=False)


class DbExpando100(DbExpando10):
    prop_10 = db.StringProperty(indexed=False)
    prop_11 = db.StringProperty(indexed=False)
    prop_12 = db.StringProperty(indexed=False)
    prop_13 = db.StringProperty(indexed=False)
    prop_14 = db.StringProperty(indexed=False)
    prop_15 = db.StringProperty(indexed=False)
    prop_16 = db.StringProperty(indexed=False)
    prop_17 = db.StringProperty(indexed=False)
    prop_18 = db.StringProperty(indexed=False)
    prop_19 = db.StringProperty(indexed=False)
    prop_20 = db.StringProperty(indexed=False)
    prop_21 = db.StringProperty(indexed=False)
    prop_22 = db.StringProperty(indexed=False)
    prop_23 = db.StringProperty(indexed=False)
    prop_24 = db.StringProperty(indexed=False)
    prop_25 = db.StringProperty(indexed=False)
    prop_26 = db.StringProperty(indexed=False)
    prop_27 = db.StringProperty(indexed=False)
    prop_28 = db.StringProperty(indexed=False)
    prop_29 = db.StringProperty(indexed=False)
    prop_30 = db.StringProperty(indexed=False)
    prop_31 = db.StringProperty(indexed=False)
    prop_32 = db.StringProperty(indexed=False)
    prop_33 = db.StringProperty(indexed=False)
    prop_34 = db.StringProperty(indexed=False)
    prop_35 = db.StringProperty(indexed=False)
    prop_36 = db.StringProperty(indexed=False)
    prop_37 = db.StringProperty(indexed=False)
    prop_38 = db.StringProperty(indexed=False)
    prop_39 = db.StringProperty(indexed=False)
    prop_40 = db.StringProperty(indexed=False)
    prop_41 = db.StringProperty(indexed=False)
    prop_42 = db.StringProperty(indexed=False)
    prop_43 = db.StringProperty(indexed=False)
    prop_44 = db.StringProperty(indexed=False)
    prop_45 = db.StringProperty(indexed=False)
    prop_46 = db.StringProperty(indexed=False)
    prop_47 = db.StringProperty(indexed=False)
    prop_48 = db.StringProperty(indexed=False)
    prop_49 = db.StringProperty(indexed=False)
    prop_50 = db.StringProperty(indexed=False)
    prop_51 = db.StringProperty(indexed=False)
    prop_52 = db.StringProperty(indexed=False)
    prop_53 = db.StringProperty(indexed=False)
    prop_54 = db.StringProperty(indexed=False)
    prop_55 = db.StringProperty(indexed=False)
    prop_56 = db.StringProperty(indexed=False)
    prop_57 = db.StringProperty(indexed=False)
    prop_58 = db.StringProperty(indexed=False)
    prop_59 = db.StringProperty(indexed=False)
    prop_60 = db.StringProperty(indexed=False)
    prop_61 = db.StringProperty(indexed=False)
    prop_62 = db.StringProperty(indexed=False)
    prop_63 = db.StringProperty(indexed=False)
    prop_64 = db.StringProperty(indexed=False)
    prop_65 = db.StringProperty(indexed=False)
    prop_66 = db.StringProperty(indexed=False)
    prop_67 = db.StringProperty(indexed=False)
    prop_68 = db.StringProperty(indexed=False)
    prop_69 = db.StringProperty(indexed=False)
    prop_70 = db.StringProperty(indexed=False)
    prop_71 = db.StringProperty(indexed=False)
    prop_72 = db.StringProperty(indexed=False)
    prop_73 = db.StringProperty(indexed=False)
    prop_74 = db.StringProperty(indexed=False)
    prop_75 = db.StringProperty(indexed=False)
    prop_76 = db.StringProperty(indexed=False)
    prop_77 = db.StringProperty(indexed=False)
    prop_78 = db.StringProperty(indexed=False)
    prop_79 = db.StringProperty(indexed=False)
    prop_80 = db.StringProperty(indexed=False)
    prop_81 = db.StringProperty(indexed=False)
    prop_82 = db.StringProperty(indexed=False)
    prop_83 = db.StringProperty(indexed=False)
    prop_84 = db.StringProperty(indexed=False)
    prop_85 = db.StringProperty(indexed=False)
    prop_86 = db.StringProperty(indexed=False)
    prop_87 = db.StringProperty(indexed=False)
    prop_88 = db.StringProperty(indexed=False)
    prop_89 = db.StringProperty(indexed=False)
    prop_90 = db.StringProperty(indexed=False)
    prop_91 = db.StringProperty(indexed=False)
    prop_92 = db.StringProperty(indexed=False)
    prop_93 = db.StringProperty(indexed=False)
    prop_94 = db.StringProperty(indexed=False)
    prop_95 = db.StringProperty(indexed=False)
    prop_96 = db.StringProperty(indexed=False)
    prop_97 = db.StringProperty(indexed=False)
    prop_98 = db.StringProperty(indexed=False)
    prop_99 = db.StringProperty(indexed=False)


#
# ndb.Models to test: 10x && 100x
#
# The `get` and `keys` methods are overridden here with the helpers in `ndb_api`.
#

# Use `ndb.StringProperty` instead of `db.StringProperty` here:
class NdbModel10(ndb_api.NdbQueryMixin, ndb.Model):
    prop_0 = ndb.StringProperty(indexed=False)
    prop_1 = ndb.StringProperty(indexed=False)
    prop_2 = ndb.StringProperty(indexed=False)
    prop_3 = ndb.StringProperty(indexed=False)
    prop_4 = ndb.StringProperty(indexed=False)
    prop_5 = ndb.StringProperty(indexed=False)
    prop_6 = ndb.StringProperty(indexed=False)
    prop_7 = ndb.StringProperty(indexed=False)
    prop_8 = ndb.StringProperty(indexed=False)
    prop_9 = ndb.StringProperty(indexed=False)


# Use `ndb.StringProperty` instead of `db.StringProperty` here:
class NdbModel100(NdbModel10):
    prop_10 = ndb.StringProperty(indexed=False)
    prop_11 = ndb.StringProperty(indexed=False)
    prop_12 = ndb.StringProperty(indexed=False)
    prop_13 = ndb.StringProperty(indexed=False)
    prop_14 = ndb.StringProperty(indexed=False)
    prop_15 = ndb.StringProperty(indexed=False)
    prop_16 = ndb.StringProperty(indexed=False)
    prop_17 = ndb.StringProperty(indexed=False)
    prop_18 = ndb.StringProperty(indexed=False)
    prop_19 = ndb.StringProperty(indexed=False)
    prop_20 = ndb.StringProperty(indexed=False)
    prop_21 = ndb.StringProperty(indexed=False)
    prop_22 = ndb.StringProperty(indexed=False)
    prop_23 = ndb.StringProperty(indexed=False)
    prop_24 = ndb.StringProperty(indexed=False)
    prop_25 = ndb.StringProperty(indexed=False)
    prop_26 = ndb.StringProperty(indexed=False)
    prop_27 = ndb.StringProperty(indexed=False)
    prop_28 = ndb.StringProperty(indexed=False)
    prop_29 = ndb.StringProperty(indexed=False)
    prop_30 = ndb.StringProperty(indexed=False)
    prop_31 = ndb.StringProperty(indexed=False)
    prop_32 = ndb.StringProperty(indexed=False)
    prop_33 = ndb.StringProperty(indexed=False)
    prop_34 = ndb.StringProperty(indexed=False)
    prop_35 = ndb.StringProperty(indexed=False)
    prop_36 = ndb.StringProperty(indexed=False)
    prop_37 = ndb.StringProperty(indexed=False)
    prop_38 = ndb.StringProperty(indexed=False)
    prop_39 = ndb.StringProperty(indexed=False)
    prop_40 = ndb.StringProperty(indexed=False)
    prop_41 = ndb.StringProperty(indexed=False)
    prop_42 = ndb.StringProperty(indexed=False)
    prop_43 = ndb.StringProperty(indexed=False)
    prop_44 = ndb.StringProperty(indexed=False)
    prop_45 = ndb.StringProperty(indexed=False)
    prop_46 = ndb.StringProperty(indexed=False)
    prop_47 = ndb.StringProperty(indexed=False)
    prop_48 = ndb.StringProperty(indexed=False)
    prop_49 = ndb.StringProperty(indexed=False)
    prop_50 = ndb.StringProperty(indexed=False)
    prop_51 = ndb.StringProperty(indexed=False)
    prop_52 = ndb.StringProperty(indexed=False)
    prop_53 = ndb.StringProperty(indexed=False)
    prop_54 = ndb.StringProperty(indexed=False)
    prop_55 = ndb.StringProperty(indexed=False)
    prop_56 = ndb.StringProperty(indexed=False)
    prop_57 = ndb.StringProperty(indexed=False)
    prop_58 = ndb.StringProperty(indexed=False)
    prop_59 = ndb.StringProperty(indexed=False)
    prop_60 = ndb.StringProperty(indexed=False)
    prop_61 = ndb.StringProperty(indexed=False)
    prop_62 = ndb.StringProperty(indexed=False)
    prop_63 = ndb.StringProperty(indexed=False)
    prop_64 = ndb.StringProperty(indexed=False)
    prop_65 = ndb.StringProperty(indexed=False)
    prop_66 = ndb.StringProperty(indexed=False)
    prop_67 = ndb.StringProperty(indexed=False)
    prop_68 = ndb.StringProperty(indexed=False)
    prop_69 = ndb.StringProperty(indexed=False)
    prop_70 = ndb.StringProperty(indexed=False)
    prop_71 = ndb.StringProperty(indexed=False)
    prop_72 = ndb.StringProperty(indexed=False)
    prop_73 = ndb.StringProperty(indexed=False)
    prop_74 = ndb.StringProperty(indexed=False)
    prop_75 = ndb.StringProperty(indexed=False)
    prop_76 = ndb.StringProperty(indexed=False)
    prop_77 = ndb.StringProperty(indexed=False)
    prop_78 = ndb.StringProperty(indexed=False)
    prop_79 = ndb.StringProperty(indexed=False)
    prop_80 = ndb.StringProperty(indexed=False)
    prop_81 = ndb.StringProperty(indexed=False)
    prop_82 = ndb.StringProperty(indexed=False)
    prop_83 = ndb.StringProperty(indexed=False)
    prop_84 = ndb.StringProperty(indexed=False)
    prop_85 = ndb.StringProperty(indexed=False)
    prop_86 = ndb.StringProperty(indexed=False)
    prop_87 = ndb.StringProperty(indexed=False)
    prop_88 = ndb.StringProperty(indexed=False)
    prop_89 = ndb.StringProperty(indexed=False)
    prop_90 = ndb.StringProperty(indexed=False)
    prop_91 = ndb.StringProperty(indexed=False)
    prop_92 = ndb.StringProperty(indexed=False)
    prop_93 = ndb.StringProperty(indexed=False)
    prop_94 = ndb.StringProperty(indexed=False)
    prop_95 = ndb.StringProperty(indexed=False)
    prop_96 = ndb.StringProperty(indexed=False)
    prop_97 = ndb.StringProperty(indexed=False)
    prop_98 = ndb.StringProperty(indexed=False)
    prop_99 = ndb.StringProperty(indexed=False)


#
# ndb.ExpandoModels to test: 10x && 100x
#
# The `get` and `keys` methods are overridden here with the helpers in `ndb_api`.
#

# Use `ndb.StringProperty` instead of `db.StringProperty` here:
class NdbExpando10(ndb_api.NdbQueryMixin, ndb.Expando):
    prop_0 = ndb.StringProperty(indexed=False)
    prop_1 = ndb.StringProperty(indexed=False)
    prop_2 = ndb.StringProperty(indexed=False)
    prop_3 = ndb.StringProperty(indexed=False)
    prop_4 = ndb.StringProperty(indexed=False)
    prop_5 = ndb.StringProperty(indexed=False)
    prop_6 = ndb.StringProperty(indexed=False)
    prop_7 = ndb.StringProperty(indexed=False)
    prop_8 = ndb.StringProperty(indexed=False)
    prop_9 = ndb.StringProperty(indexed=False)


# Use `ndb.StringProperty` instead of `db.StringProperty` here:
class NdbExpando100(NdbExpando10):
    prop_10 = ndb.StringProperty(indexed=False)
    prop_11 = ndb.StringProperty(indexed=False)
    prop_12 = ndb.StringProperty(indexed=False)
    prop_13 = ndb.StringProperty(indexed=False)
    prop_14 = ndb.StringProperty(indexed=False)
    prop_15 = ndb.StringProperty(indexed=False)
    prop_16 = ndb.StringProperty(indexed=False)
    prop_17 = ndb.StringProperty(indexed=False)
    prop_18 = ndb.StringProperty(indexed=False)
    prop_19 = ndb.StringProperty(indexed=False)
    prop_20 = ndb.StringProperty(indexed=False)
    prop_21 = ndb.StringProperty(indexed=False)
    prop_22 = ndb.StringProperty(indexed=False)
    prop_23 = ndb.StringProperty(indexed=False)
    prop_24 = ndb.StringProperty(indexed=False)
    prop_25 = ndb.StringProperty(indexed=False)
    prop_26 = ndb.StringProperty(indexed=False)
    prop_27 = ndb.StringProperty(indexed=False)
    prop_28 = ndb.StringProperty(indexed=False)
    prop_29 = ndb.StringProperty(indexed=False)
    prop_30 = ndb.StringProperty(indexed=False)
    prop_31 = ndb.StringProperty(indexed=False)
    prop_32 = ndb.StringProperty(indexed=False)
    prop_33 = ndb.StringProperty(indexed=False)
    prop_34 = ndb.StringProperty(indexed=False)
    prop_35 = ndb.StringProperty(indexed=False)
    prop_36 = ndb.StringProperty(indexed=False)
    prop_37 = ndb.StringProperty(indexed=False)
    prop_38 = ndb.StringProperty(indexed=False)
    prop_39 = ndb.StringProperty(indexed=False)
    prop_40 = ndb.StringProperty(indexed=False)
    prop_41 = ndb.StringProperty(indexed=False)
    prop_42 = ndb.StringProperty(indexed=False)
    prop_43 = ndb.StringProperty(indexed=False)
    prop_44 = ndb.StringProperty(indexed=False)
    prop_45 = ndb.StringProperty(indexed=False)
    prop_46 = ndb.StringProperty(indexed=False)
    prop_47 = ndb.StringProperty(indexed=False)
    prop_48 = ndb.StringProperty(indexed=False)
    prop_49 = ndb.StringProperty(indexed=False)
    prop_50 = ndb.StringProperty(indexed=False)
    prop_51 = ndb.StringProperty(indexed=False)
    prop_52 = ndb.StringProperty(indexed=False)
    prop_53 = ndb.StringProperty(indexed=False)
    prop_54 = ndb.StringProperty(indexed=False)
    prop_55 = ndb.StringProperty(indexed=False)
    prop_56 = ndb.StringProperty(indexed=False)
    prop_57 = ndb.StringProperty(indexed=False)
    prop_58 = ndb.StringProperty(indexed=False)
    prop_59 = ndb.StringProperty(indexed=False)
    prop_60 = ndb.StringProperty(indexed=False)
    prop_61 = ndb.StringProperty(indexed=False)
    prop_62 = ndb.StringProperty(indexed=False)
    prop_63 = ndb.StringProperty(indexed=False)
    prop_64 = ndb.StringProperty(indexed=False)
    prop_65 = ndb.StringProperty(indexed=False)
    prop_66 = ndb.StringProperty(indexed=False)
    prop_67 = ndb.StringProperty(indexed=False)
    prop_68 = ndb.StringProperty(indexed=False)
    prop_69 = ndb.StringProperty(indexed=False)
    prop_70 = ndb.StringProperty(indexed=False)
    prop_71 = ndb.StringProperty(indexed=False)
    prop_72 = ndb.StringProperty(indexed=False)
    prop_73 = ndb.StringProperty(indexed=False)
    prop_74 = ndb.StringProperty(indexed=False)
    prop_75 = ndb.StringProperty(indexed=False)
    prop_76 = ndb.StringProperty(indexed=False)
    prop_77 = ndb.StringProperty(indexed=False)
    prop_78 = ndb.StringProperty(indexed=False)
    prop_79 = ndb.StringProperty(indexed=False)
    prop_80 = ndb.StringProperty(indexed=False)
    prop_81 = ndb.StringProperty(indexed=False)
    prop_82 = ndb.StringProperty(indexed=False)
    prop_83 = ndb.StringProperty(indexed=False)
    prop_84 = ndb.StringProperty(indexed=False)
    prop_85 = ndb.StringProperty(indexed=False)
    prop_86 = ndb.StringProperty(indexed=False)
    prop_87 = ndb.StringProperty(indexed=False)
    prop_88 = ndb.StringProperty(indexed=False)
    prop_89 = ndb.StringProperty(indexed=False)
    prop_90 = ndb.StringProperty(indexed=False)
    prop_91 = ndb.StringProperty(indexed=False)
    prop_92 = ndb.StringProperty(indexed=False)
    prop_93 = ndb.StringProperty(indexed=False)
    prop_94 = ndb.StringProperty(indexed=False)
    prop_95 = ndb.StringProperty(indexed=False)
    prop_96 = ndb.StringProperty(indexed=False)
    prop_97 = ndb.StringProperty(indexed=False)
    prop_98 = ndb.StringProperty(indexed=False)
    prop_99 = ndb.StringProperty(indexed=False)
