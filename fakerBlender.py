import bpy
from bpy.types import NodeTree, Node, NodeSocket
from faker import Faker

fake = Faker()
Faker.seed(0)

# Implementation of custom nodes from Python


# Derived from the NodeTree base type, similar to Menu, Operator, Panel, etc.
class MyCustomTree(NodeTree):
    # Description string
    '''A custom node tree type that will show up in the editor type list'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'CustomTreeType'
    # Label for nice name display
    bl_label = "Custom Node Tree"
    # Icon identifier
    bl_icon = 'NODETREE'


 


# Mix-in class for all custom nodes in this tree type.
# Defines a poll function to enable instantiation.
class MyCustomTreeNode:
    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'CustomTreeType'


 
    
#------------------------------------------------------------------------------

# string type
class MyCustomStringNode(Node, MyCustomTreeNode):
    bl_idname = 'CustomNodeStringType'
    bl_label  = 'Custom String Node'
    
    my_string_prop: bpy.props.StringProperty()
    
    def init(self, context):
        self.inputs.new('NodeSocketString', "Name")
        
        self.outputs.new('NodeSocketString', "Name")
        

# integer type
class MyCustomIntNode(Node, MyCustomTreeNode):
    bl_idname = 'CustomNodeIntType'
    bl_label  = 'Custom Int Node'
    
    my_int_prop: bpy.props.IntProperty()
    
    def init(self, context):
        self.inputs.new('NodeSocketInt', 'Number')
        
        self.outputs.new('NodeSocketInt', 'Number')
        
    def update(self):
        print('Updating node: ', self.name)
           
        self.outputs['Number'].default_value  = self.inputs['Number'].default_value
            
        print('process output links...')
        for link in self.outputs['Number'].links:
            print('processing out links - ', link.to_node.name)
            link.to_socket.default_value = self.outputs['Number'].default_value
        
# person type      
class MyCustomPersonNode(Node, MyCustomTreeNode):
    bl_idname = 'CustomNodePersonType'
    bl_label  = 'Person Node'

    
    #nameIn = bpy.props.StringProperty()
    #nameOut = bpy.props.StringProperty()
    
    def init(self, context):
        self.inputs.new('NodeSocketString', 'Name')
        
        self.outputs.new('NodeSocketString', 'Name')
        
    def update(self):
        self.inputs['Name'].default_value = fake.name()
        
        if 'Name' in self.outputs:
            # out prop exists
            self.outputs['Name'].default_value = self.inputs['Name'].default_value
        
            for link in self.outputs['Name'].links:
                print('processing out links for Name - ', link.to_node.name)
                link.to_socket.default_value = self.outputs['Name'].default_value
        
# address type
class MyCustomAddressNode(Node, MyCustomTreeNode):
    bl_idname = 'CustomNodeAddressType'
    bl_label = 'Address Node'
    
    def init(self, context):
        self.inputs.new('NodeSocketString', 'House Number')
        self.inputs.new('NodeSocketString', "Street")
        self.inputs.new('NodeSocketString', 'City')
        self.inputs.new('NodeSocketString', 'ZipCode')
        
        self.outputs.new('NodeSocketString', 'Address')
        
    def update(self):
        self.inputs['House Number'].default_value = fake.building_number()
        
        if 'Street' in self.inputs:
            self.inputs['Street'].default_value = fake.street_name()
            
        if 'City' in self.inputs:
            self.inputs['City'].default_value = fake.city()
            
        if 'ZipCode' in self.inputs:
            self.inputs['ZipCode'].default_value = fake.postcode()
        
        if 'Address' in self.outputs:
            #prop exists
            # assemble the address from different attributes
            street = self.inputs['House Number'].default_value \
            + ' ' + self.inputs['Street'].default_value
            
            cp = self.inputs['City'].default_value + ' ' + \
            self.inputs['ZipCode'].default_value
            
            out_address = '\n'.join([street, cp])
            
            self.outputs['Address'].default_value = out_address
            
            # process out links
            for link in self.outputs['Address'].links:
                print('processing out links for Name - ', link.to_node.name)
                link.to_socket.default_value = self.outputs['Address'].default_value
        

# phone number +1 (408) 777 888 x3456
class MyCustomPhoneNumber(Node, MyCustomTreeNode):
    bl_idname = 'CustomNodePNumberType'
    bl_label = 'Phone Number'
    
    country_code_string_prop = bpy.props.StringProperty()
    phone_num_string_prop = bpy.props.StringProperty()
    extn_int_prop = bpy.props.IntProperty()
    
    def init(self, context):
        self.inputs.new('NodeSocketString', 'Country Code')
        self.inputs.new('NodeSocketString',  'Phone Number')
        #self.inputs.new('NodeSocketInt',     'Extension')
        
        self.outputs.new('NodeSocketString', 'Phone Number')
        
    def update(self):
        self.inputs['Country Code'].default_value = fake.country_calling_code()
        
        if 'Phone Number' in self.inputs:
            self.inputs['Phone Number'].default_value = fake.phone_number()
        
        if 'Phone Number' in self.outputs:
            #prop exists
            out = self.inputs['Country Code'].default_value + ' ' + \
            self.inputs['Phone Number'].default_value
            
            self.outputs['Phone Number'].default_value = out
            
            # process out links
            for link in self.outputs['Phone Number'].links:
                print('processing out links for Name - ', link.to_node.name)
                link.to_socket.default_value = self.outputs['Phone Number'].default_value
            
            
        
#Company Name, XYZ, LLC
class MyCustomCompanyName(Node, MyCustomTreeNode):
    bl_idname = 'CustomNodeCNameType'
    bl_label = 'Company Name'
        
    comp_name_string_prop = bpy.props.StringProperty()
    
    def init(self, context):
        self.inputs.new('NodeSocketString', 'Company Name')
        self.inputs.new('NodeSocketString',  'Suffix')
        
        self.outputs.new('NodeSocketString', 'Company Name')
        
#Bank Account Number, Citibank, Acct Num
class MyCustomBankAccount(Node, MyCustomTreeNode):
    bl_idname = 'CustomNodeBAccountType'
    bl_label = 'Bank Account'
    
    bank_name = bpy.props.StringProperty()
    bank_acct_num = bpy.props.StringProperty()
    
    def init(self, context):
        self.inputs.new('NodeSocketString', 'Bank Name')
        self.inputs.new('NodeSocketString', 'Account Number')
        
        self.outputs.new('NodeSocketString', 'Account Number')
        

# Credit Card Info.
# 'Discover\nKatherine Fisher\n6587647593824218 05/26\nCVC: 892\n'
class MyCustomCreditCard(Node, MyCustomTreeNode):
    bl_idname = 'CustomCCType'
    bl_label = 'Credit Card'
    
    card_type = bpy.props.StringProperty()
    card_num  = bpy.props.IntProperty()
    card_exp  = bpy.props.StringProperty()
    card_cvv  = bpy.props.IntProperty()
    
    def init(self, context):
        self.inputs.new('NodeSocketString', 'Type')
        self.inputs.new('NodeSocketInt', 'Number')
        self.inputs.new('NodeSocketString', 'Expiry')
        self.inputs.new('NodeSocketInt', 'CVV')
        
        self.outputs.new('NodeSocketInt', 'Number')
        

# Social Security Number (SSN)
# 498-52-4970
class MyCustomSSN(Node, MyCustomTreeNode):
    bl_idname = 'CustomSSN'
    bl_label  = 'SSN'
    
    #id  = bpy.props.StringProperty()
    #ssn = bpy.props.IntProperty()
    
    def init(self, context):
        self.inputs.new('NodeSocketString', 'ID')
        self.outputs.new('NodeSocketInt', 'SSN')

    def process(self, context):
        print(f'inputs: {self.inputs}')
        print(f'outputs: {self.outputs}')
        
    def update(self):
        print('Updating node: ', self.name)
        print('input value:', self.inputs['ID'].default_value)
        
        # get the SSN from faker
        self.inputs['ID'].default_value = fake.ssn()
        
        inp_val = self.inputs['ID'].default_value
        if inp_val and inp_val.strip():
            # not blank
            #print('...processing...')
            #print('input value: ', self.inputs['ID'].default_value)
            val = inp_val.replace('-', '')
            
            if 'SSN' in self.outputs:
                # found the property
                self.outputs['SSN'].default_value = int(val)
        
                #print('Result SSN:', self.outputs['SSN'].default_value
                #print('process output links...')
                for link in self.outputs['SSN'].links:
                    print('processing out links SSN - ', link.to_node.name)
                    link.to_socket.default_value = self.outputs['SSN'].default_value
                
        
    def execute(self, context):
        print('I am at execute()')
        
     


    
 
    


#------------------------------------------------------------------------------
### Node Categories ###
# Node categories are a python system for automatically
# extending the Add menu, toolbar panels and search operator.
# For more examples see release/scripts/startup/nodeitems_builtins.py

import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem

# our own base class with an appropriate poll function,
# so the categories only show up in our own tree type


class MyNodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        #return context.space_data.tree_type == 'CustomTreeType'
        return context.space_data.tree_type == 'CompositorNodeTree'


# all categories in a list
node_categories = [
    # identifier, label, items list
#    MyNodeCategory('SOMENODES', "Some Nodes", items=[
#        # our basic node
#        NodeItem("CustomNodeType"),
#    ]),
#    MyNodeCategory('OTHERNODES', "Other Nodes", items=[
#        # the node item can have additional settings,
#        # which are applied to new nodes
#        # NOTE: settings values are stored as string expressions,
#        # for this reason they should be converted to strings using repr()
#        NodeItem("CustomNodeType", label="Node A", settings={
#            "my_string_prop": repr("Lorem ipsum dolor sit amet"),
#            "my_float_prop": repr(1.0),
#        }),
#        NodeItem("CustomNodeType", label="Node B", settings={
#            "my_string_prop": repr("consectetur adipisicing elit"),
#            "my_float_prop": repr(2.0),
#        }),
#    ]),
    MyNodeCategory('FakerNodes', 'Faker Library Nodes', items=[
        # nodes
        NodeItem('CustomNodePersonType',  label='Person'),
        NodeItem('CustomNodeAddressType', label='Address'),
        NodeItem('CustomNodePNumberType', label='Phone Number'),
        NodeItem('CustomNodeCNameType', label='Company Name'),
        NodeItem('CustomNodeBAccountType', label='Bank Account'),
        NodeItem('CustomSSN', label = 'SSN'),
        NodeItem('CustomCCType', label = 'Credit Card'),
        #NodeItem('CustomNodeStringType', label='Name'),
        #NodeItem('CustomNodeIntType', label='House Number'),
        #NodeItem('CustomNodeStringType', label='Street Name'),
        NodeItem('CustomNodeStringType', label= 'String'),
        NodeItem('CustomNodeIntType', label='Integer'),
        
    
    ]),
]

classes = (
    MyCustomTree,
    #MyCustomSocket,
    #MyCustomNode,
    MyCustomStringNode,
    MyCustomIntNode,
    MyCustomPersonNode,
    MyCustomAddressNode,
    MyCustomPhoneNumber,
    MyCustomCompanyName,
    MyCustomBankAccount,
    MyCustomCreditCard,
    MyCustomSSN,
    
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    nodeitems_utils.register_node_categories('CUSTOM_NODES', node_categories)


def unregister():
    nodeitems_utils.unregister_node_categories('CUSTOM_NODES')

    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == "__main__":
    register()

#tst = bpy.ops.node.add_node(type="CustomSSN")


