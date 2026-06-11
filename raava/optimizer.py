# Imports
from typing import List, Dict, Any
from raava.ir import IROpCode, IRInstruction

# Optimizer class
class Optimizer:
    
    # Main optimize entry method
    def optimize ( self , instructions : List [ IRInstruction ] ) -> List [ IRInstruction ] :
        
        # 1. Run constant folding & propagation
        folded_instructions = self.fold_constants ( instructions )
        
        # 2. Run dead code elimination to clean up unused compiler temporaries
        final_instructions = self.eliminate_dead_code ( folded_instructions )
        
        return final_instructions
        
    # Constant folding pass method
    def fold_constants ( self , instructions : List [ IRInstruction ] ) -> List [ IRInstruction ] :
        
        const_map : Dict [ str , Any ] = { }
        optimized : List [ IRInstruction ] = [ ]
        
        for instr in instructions :
            
            # Copy instruction object so we don't modify the original list in place
            new_instr = IRInstruction (
                opcode = instr.opcode ,
                result = instr.result ,
                arg1 = instr.arg1 ,
                arg2 = instr.arg2 ,
                value = instr.value
            )
            
            if new_instr.opcode == IROpCode.CONST :
                
                if new_instr.result is not None :
                    
                    const_map [ new_instr.result ] = new_instr.value
                    
                optimized.append ( new_instr )
                
            elif new_instr.opcode == IROpCode.COPY :
                
                # Propagate constant if source operand is constant
                if new_instr.arg1 in const_map :
                    
                    val = const_map [ new_instr.arg1 ]
                    new_instr.opcode = IROpCode.CONST
                    new_instr.value = val
                    new_instr.arg1 = None
                    
                    if new_instr.result is not None :
                        
                        const_map [ new_instr.result ] = val
                        
                else :
                    
                    if new_instr.result is not None and new_instr.result in const_map :
                        
                        del const_map [ new_instr.result ]
                        
                optimized.append ( new_instr )
                
            elif new_instr.opcode == IROpCode.BINARY_OP :
                
                # Propagate constant inputs
                left_val = const_map.get ( new_instr.arg1 ) if new_instr.arg1 in const_map else None
                right_val = const_map.get ( new_instr.arg2 ) if new_instr.arg2 in const_map else None
                
                if new_instr.arg1 in const_map and new_instr.arg2 in const_map :
                    
                    try :
                        
                        folded_val = self.evaluate_bin_op ( left_val , new_instr.value , right_val )
                        new_instr.opcode = IROpCode.CONST
                        new_instr.value = folded_val
                        new_instr.arg1 = None
                        new_instr.arg2 = None
                        
                        if new_instr.result is not None :
                            
                            const_map [ new_instr.result ] = folded_val
                            
                    except Exception :
                        
                        if new_instr.result is not None and new_instr.result in const_map :
                            
                            del const_map [ new_instr.result ]
                            
                else :
                    
                    if new_instr.result is not None and new_instr.result in const_map :
                        
                        del const_map [ new_instr.result ]
                        
                optimized.append ( new_instr )
                
            elif new_instr.opcode == IROpCode.UNARY_OP :
                
                if new_instr.arg1 in const_map :
                    
                    try :
                        
                        val = const_map [ new_instr.arg1 ]
                        folded_val = self.evaluate_unary_op ( new_instr.value , val )
                        new_instr.opcode = IROpCode.CONST
                        new_instr.value = folded_val
                        new_instr.arg1 = None
                        
                        if new_instr.result is not None :
                            
                            const_map [ new_instr.result ] = folded_val
                            
                    except Exception :
                        
                        if new_instr.result is not None and new_instr.result in const_map :
                            
                            del const_map [ new_instr.result ]
                            
                else :
                    
                    if new_instr.result is not None and new_instr.result in const_map :
                        
                        del const_map [ new_instr.result ]
                        
                optimized.append ( new_instr )
                
            else :
                
                # If a variable is redefined, invalidate its constant mapping
                if new_instr.result is not None and new_instr.result in const_map :
                    
                    del const_map [ new_instr.result ]
                    
                optimized.append ( new_instr )
                
        return optimized
        
    # Dead code elimination pass method
    def eliminate_dead_code ( self , instructions : List [ IRInstruction ] ) -> List [ IRInstruction ] :
        
        uses : Dict [ str , int ] = { }
        
        # 1. Count uses of all variables/temporaries
        for instr in instructions :
            
            if instr.arg1 is not None and isinstance ( instr.arg1 , str ) :
                
                uses [ instr.arg1 ] = uses.get ( instr.arg1 , 0 ) + 1
                
            if instr.arg2 is not None and isinstance ( instr.arg2 , str ) :
                
                uses [ instr.arg2 ] = uses.get ( instr.arg2 , 0 ) + 1
                
            # If function call, check arguments
            if instr.opcode == IROpCode.CALL and isinstance ( instr.arg2 , list ) :
                
                for arg in instr.arg2 :
                    
                    if isinstance ( arg , str ) :
                        
                        uses [ arg ] = uses.get ( arg , 0 ) + 1
                        
        # 2. Filter out assignments to unused compiler-generated temporaries
        optimized : List [ IRInstruction ] = [ ]
        
        for instr in instructions :
            
            if instr.result is not None and instr.result.startswith ( 't' ) :
                
                if uses.get ( instr.result , 0 ) == 0 :
                    
                    continue  # Dead code eliminated!
                    
            optimized.append ( instr )
            
        return optimized
        
    # Binary operations evaluator method
    def evaluate_bin_op ( self , v1 : Any , op : str , v2 : Any ) -> Any :
        
        if op == '+' :
            return v1 + v2
        elif op == '-' :
            return v1 - v2
        elif op == '*' :
            return v1 * v2
        elif op == '/' :
            if isinstance ( v1 , int ) and isinstance ( v2 , int ) :
                return v1 // v2
            return v1 / v2
        elif op == '==' :
            return v1 == v2
        elif op == '!=' :
            return v1 != v2
        elif op == '<' :
            return v1 < v2
        elif op == '>' :
            return v1 > v2
        elif op == '<=' :
            return v1 <= v2
        elif op == '>=' :
            return v1 >= v2
        elif op == 'and' :
            return v1 and v2
        elif op == 'or' :
            return v1 or v2
        raise Exception ( f"Unknown binary operator '{ op }'" )
        
    # Unary operations evaluator method
    def evaluate_unary_op ( self , op : str , v : Any ) -> Any :
        
        if op == '-' :
            return -v
        elif op == 'not' :
            return not v
        raise Exception ( f"Unknown unary operator '{ op }'" )
