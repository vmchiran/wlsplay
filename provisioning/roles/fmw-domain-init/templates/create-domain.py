domain_application_home = '{{ applications_home }}/{{ domain_name }}'
domain_configuration_home = '{{ domains_home }}/{{ domain_name }}'
domain_name = '{{ domain_name }}'
java_home = '{{ jdk_home }}'
middleware_home = '{{ middleware_home }}'

weblogic_home = '{{ weblogic_home }}'
weblogic_admin= '{{ weblogic_admin }}'
weblogic_admin_pass= '{{ weblogic_admin_pass }}'

weblogic_template=weblogic_home + '/common/templates/domains/wls.jar'

readTemplate(weblogic_template)
setOption('DomainName', domain_name)
setOption('OverwriteDomain', 'true')
setOption('JavaHome', java_home)
## ServerStartMode can be: dev, prod. Default: dev
setOption('ServerStartMode', 'prod')
setOption('AppDir', domain_application_home)

cd('/Security/base_domain/User/weblogic')
cmo.setName(weblogic_admin)
cmo.setUserPassword(weblogic_admin_pass)
cd('/')

writeDomain(domain_configuration_home)
closeTemplate()
