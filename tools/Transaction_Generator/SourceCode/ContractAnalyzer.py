import slither

def getParameterType(parameter):
    if hasattr(parameter, 'type'):
        if hasattr(parameter.type, 'name'):
            return parameter.type.name
        elif hasattr(parameter.type, 'type'):
            return [getParameterType(parameter.type)]
        else:
            return parameter.type
    else:
        return parameter

def analyze_contract(contractFile):
    slitherInstance = slither.Slither(contractFile)
    results = {}

    # Fet all funtions
    contracts = slitherInstance.contracts
    main_contract = ''
    constructorInfo = None

    # Interate contracts
    for contract in contracts:
        if (not contract.is_fully_implemented) or contract.is_interface or contract.is_library:
            continue
        
        if contract.derived_contracts == []:
            main_contract = contract.name
            if contract.constructor != None:
                constructor = contract.constructor
                constructorInfo = {
                    "full_name": constructor.full_name,
                    "name": 'constructor',
                    "visibility": constructor.visibility,
                    "payable": constructor.payable
                }
                
                constructorParameters = {}
                for parameter in constructor.parameters:
                    constructorParameters[parameter.name] = getParameterType(parameter)

                constructorInfo["parameters"] = constructorParameters

                # Get internal calls
                internalCalls = []

                # Interate fintions internally called by this function
                for ir in constructor._internal_calls:
                    internalCalls.append(ir.name)

                # Get state variables written by this function
                reads = []
                writes = []
                for ir in constructor.state_variables_read:
                    reads.append(ir.full_name)
                
                for ir in constructor.state_variables_written:
                    writes.append(ir.full_name)
                
                constructorInfo["internalCalls"] = internalCalls
                constructorInfo["reads"] = reads
                constructorInfo["writes"] = writes

                results['constructor'] = constructorInfo
     
        for function in contract.functions:
            if function.name == 'slitherConstructorVariables' or function.name == 'receive' or function.is_constructor or function.is_constructor_variables:
                continue

            funcInfo = {
                "full_name": function.full_name,
                "name": function.name,
                "visibility": function.visibility,
                "payable": function.payable
            }

            parameters = {}

            for parameter in function.parameters:
                parameters[parameter.name] = getParameterType(parameter)

            funcInfo["parameters"] = parameters

            # Get internal calls
            internalCalls = []

            # Interate fintions internally called by this function
            for ir in function._internal_calls:
                internalCalls.append(ir.name)

            # Get state variables written by this function
            reads = []
            writes = []
            for ir in function.state_variables_read:
                reads.append(ir.full_name)
            
            for ir in function.state_variables_written:
                writes.append(ir.full_name)
            
            funcInfo["internalCalls"] = internalCalls
            funcInfo["reads"] = reads
            funcInfo["writes"] = writes

            results[function.name] = funcInfo

    return main_contract, results