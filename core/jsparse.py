# import esprima

# # ast = esprima.parseScript('CONFIG_USER_RTK_BRIDGE_MODE')
# # ast = esprima.parseScript('defined(CONFIG_GPON_FEATURE)')
# # ast = esprima.parseScript('defined(CONFIG_GPON_FEATURE) || defined(CONFIG_EPON_FEATURE)')
# # ast = esprima.parseScript('defined(CONFIG_IPV6) && defined(CONFIG_USER_RADVD)')
# # ast = esprima.parseScript('CONFIG_RTK_VOIP_CON_CH_NUM > 1')
# # ast = esprima.parseScript('CONFIG_RTK_VOIP_CON_CH_NUM == 1')
# # print(ast)

# def get_value(key):
#   # todo 根据C中定义的变量进行值返回
#   return True

# def parse(statement):
#   try:
#     ast = esprima.parseScript(statement)
#     if len(ast.body) == 0:
#       return False

#     return ast.body[1]
#   except:
#     return False

# def identifier(key):
#   return get_value(key)

# def call_expression(ast):
#   if(len(ast.arguments) == 0):
#     return False;
#   if ast.callee.name == 'defined':
#     key = ast.arguments[0].name
#     return get_value(key)

# def analyse(ast):
#   ast = ast.expression
#   type = ast.type
#   if type == 'Identifier':
#     return identifier(ast.name)
#   elif type == 'CallExpression':
#     return call_expression(ast)
#   else:
#     pass