ADDON_NAME='suitecrm'
FULL_ADDON_NAME='fab_addon_' + ADDON_NAME
SQLALCHEMY_BINDS = {
    'suitecrm': 'mysql://bisio:lollipop300777@10.133.33.77/suitecrm',
    'crm_ext': 'mysql://root:lollipop300777@localhost/crm_ext'
}
#ADDON_MANAGERS = ['fab_addon_suitecrm.manager.MyAddOnManager']