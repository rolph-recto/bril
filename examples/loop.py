### project 2 Loop Detection

import json
import sys

from cfg import *
from form_blocks import *
from dom import *
from df import *


### detect back-edges
def get_backedges(successors,domtree):
  backedges = set()
  for source,sinks in successors.items():
    for sink in sinks:
      if sink in domtree[source]:
        backedges.add((source,sink))

  return backedges


### get natural loops
def loopsy(source,sink,predecessors):
<<<<<<< HEAD
    worklist = [source]
    loop = set()
    while len(worklist)>0:
        current = worklist.pop()
        pr = predecessors[current]
        for p in pr:
            if not(p in loop or p==sink):
                loop.add(p)
                worklist.append(p)
    loop.add(sink)
    loop.add(source)
    return loop


<<<<<<< HEAD
### find all the natural loops
def natloops(blocks):
  pred,succ = edges(blocks)
  dom = get_dom(succ,list(blocks.keys())[0])
  for source,sink in get_backedges(succ,dom):
    yield loopsy(source,sink,pred)


### get all reaching definitions
=======
  worklist = [source]
  loop = set()
  while len(worklist)>0:
    current = worklist.pop()
    pr = predecessors[current]
    for p in pr:
      if not(p in loop or p==sink):
        loop.add(p)
        worklist.append(p)

  loop.add(sink)
  loop.add(source)
  return loop


### apply reaching definitions analysis
>>>>>>> c04226ddf403fc9a006c79f8d078c825897d881c
=======
>>>>>>> parent of cdac03f... Commented code
def reachers(blocks):
  rins, routs = df_worklist(blocks, ANALYSIS["rdef"])
  return rins,routs


### get variable information for reaching definitions
def reaching_def_vars(blocks, reaching_defs):
  rdef_vars = {}

  for blockname, rdefs_block in reaching_defs.items():
    block = blocks[blockname]
    block_rdef_vars = [] 
    for rdef_blockid, rdef_instr in rdefs_block:
      block_rdef_vars.append( \
          (rdef_blockid, rdef_instr, blocks[rdef_blockid][rdef_instr]["dest"]))

    rdef_vars[blockname] = block_rdef_vars

  return rdef_vars

<<<<<<< HEAD
<<<<<<< HEAD
### detect LI instructions for a single natural loop
=======
# detect LI instructions for a single natural loop
>>>>>>> parent of cdac03f... Commented code
def invloop(blocks,rdef_var_ins,rdef_var_outs,natloop):
    boolmap = {}
    worklist = []
    for blockname in natloop:
        boolmap[blockname] = [False for i in range(len(blocks[blockname]))]
        worklist.append(blockname)

    while len(worklist)>0:
      blockname = worklist.pop()
      block = blocks[blockname]

      boolmap_block = []
      for instr in block:
        # assignment of a constant to a variable
        if "dest" in instr and "value" in instr:
          boolmap_block.append(True)

        # assignment of a computation to a variable
        elif "dest" in instr and "args" in instr:
          # for each argument, either one of the following has to be true:
          # * all reaching defs of the argument are outside the loop
          # * there is exactly one reaching def for the argument in the loop
          instr_loop_invariant = True
          for arg in instr["args"]:
            var = instr["dest"]
            var_rdefs = list(filter(lambda rdef: rdef[2] == var, \
                rdef_var_ins[blockname]))
          
            var_rdefs_blocks = \
                map(lambda rdef: rdef[0] not in natloop, var_rdefs)

            rdefs_outside = all(var_rdefs_blocks)

            single_rdef = False
            if len(var_rdefs) == 1:
              rdef_block, rdef_instr, _ = var_rdefs[0]
              if rdef_block in natloop:
                single_rdef = boolmap[rdef_block][rdef_instr]

            instr_loop_invariant = \
                instr_loop_invariant and (rdefs_outside or single_rdef)

          boolmap_block.append(instr_loop_invariant)

        else:
          boolmap_block.append(False)
      
      boolmap[blockname] = boolmap_block


    # is it loop invariant 
    # does it dominate all uses
    # no other definitions of same variable
    # dominates all loop exits
    return boolmap

### move stuff
def codemot(bril):
  for func in bril['functions']:
    blocks = block_map(form_blocks(func['instrs']))
    add_terminators(blocks)
    rins, routs = reachers(blocks) # what is reaching
    rdef_var_ins  = reaching_def_vars(blocks, rins)
    rdef_var_outs = reaching_def_vars(blocks, rins)

    for natloop in natloops(blocks):
      boolmap = invloop(blocks,rdef_var_ins,rdef_var_outs,natloop) 

def natloops(blocks): #input backedge
  pred,succ = edges(blocks)
  dom = get_dom(succ,list(blocks.keys())[0])
  for source,sink in get_backedges(succ,dom):
    yield loopsy(source,sink,pred) # natloops

def printstuffs(bril):
=======

# detect loop-invariant instructions for a single natural loop
def invloop(blocks,rdef_var_ins,rdef_var_outs,natloop):
  boolmap = {}
  worklist = []
  for blockname in natloop:
    boolmap[blockname] = [False for i in range(len(blocks[blockname]))]
    worklist.append(blockname)

  while len(worklist)>0:
    blockname = worklist.pop()
    block = blocks[blockname]

    boolmap_block = []
    for instr in block:
      # assignment of a constant to a variable
      if "dest" in instr and "value" in instr:
        boolmap_block.append(True)

      # assignment of a computation to a variable
      elif "dest" in instr and "args" in instr:
        # for each argument, either one of the following has to be true:
        # 1) all reaching defs of the argument are outside the loop
        # * there is exactly one reaching def for the argument in the loop
        instr_loop_invariant = True
        for arg in instr["args"]:
          var = instr["dest"]

          # condition 1
          var_rdefs = list(filter(lambda rdef: rdef[2] == var, \
              rdef_var_ins[blockname]))
        
          var_rdefs_blocks = \
              map(lambda rdef: rdef[0] not in natloop, var_rdefs)

          rdefs_outside = all(var_rdefs_blocks)

          # condition 2
          single_rdef = False
          if len(var_rdefs) == 1:
            rdef_block, rdef_instr, _ = var_rdefs[0]
            if rdef_block in natloop:
              single_rdef = boolmap[rdef_block][rdef_instr]

          instr_loop_invariant = \
              instr_loop_invariant and (rdefs_outside or single_rdef)

        boolmap_block.append(instr_loop_invariant)

      else:
        boolmap_block.append(False)
    
    boolmap[blockname] = boolmap_block

  return boolmap


### get exits for a natural loop
def loop_exits(blocks, succ, natloop):
  exits = []
  for blockname in natloop:
    for successor in succ[blockname]:
      if successor not in natloop:
        exits.append(successor)

  return exits


### check hoisting conditions for loop-invariant instruction
def can_hoist(blocks, succ, domtree, rdef_var_ins, rdef_var_outs, \
              natloop, blockname, instr_ind):

  # condition 1: instruction dominates all loop exits
  dominates_exits = True
  exits = loop_exits(blocks, succ, natloop)
  for exit in exits:
    dominates_exits = dominates_exits and blockname in domtree[exit]

  # condition 2: the instruction is the only definition for that var in the loop
  instr = blocks[blockname][instr_ind]
  var = instr["dest"]
  only_definition = True
  for loop_blockname in natloop:
    for rdef_blockid,rdef_instr,rdef_var in rdef_var_outs[loop_blockname]:
      if rdef_var == var \
         and rdef_blockid in natloop \
         and (rdef_blockid != blockname or rdef_instr != instr_ind):
        only_definition = False

  # condition 3: definition dominates all its uses
  # TODO: actually implement this
  dominates_uses = True

  return dominates_exits and only_definition and dominates_uses


### compute which instructions can be hoisted into the preheader
def hoistloop(blocks, succ, domtree, rdef_var_ins, rdef_var_outs, natloop, invmap):
  hoistmap = {}
  for blockname in natloop:
    invblock = invmap[blockname]
    hoistmap_block = []
    for i,loop_invariant in enumerate(invblock):
      if loop_invariant:
        hoistable = can_hoist(blocks, succ, domtree, rdef_var_ins, \
            rdef_var_outs, natloop, blockname, i)
        hoistmap_block.append(hoistable)

      else:
        hoistmap_block.append(False)

    hoistmap[blockname] = hoistmap_block

  return hoistmap


### build preheader for natural loop
def build_preheader(blocks, natloop, hoistmap):
  preheader = []
  for blockname in natloop:
    for i,instr in enumerate(blocks[blockname]):
      if hoistmap[blockname][i]:
        preheader.append(instr)

  return preheader


### hoist instructions out of blocks
def hoist_instructions(blocks, natloop, hoistmap):
  natloop_blocks = {}
  for blockname in natloop:
    block = []
    for i,instr in enumerate(blocks[blockname]):
      if not hoistmap[blockname][i]:
        block.append(instr)

    natloop_blocks[blockname] = block

  return natloop_blocks


### calculate fallthroughs of blocks
def get_fallthroughs(blocks, succ):
  fallthrough_map = {}
  for blockname, block in blocks.items():
    jmp_targets = []
    for instr in block:
      if instr["op"] == "jmp":
        jmp_targets.append(instr["args"][0])

      elif instr["op"] == "br":
        jmp_targets.append(instr["args"][1])
        jmp_targets.append(instr["args"][2])

    succ_minus_targets = [s for s in succ[blockname] if s not in jmp_targets]
    if len(succ_minus_targets) > 0:
      fallthrough_map[blockname] = succ_minus_targets[0]

  return fallthrough_map


### order basic blocks according to the following constraints:
### * fallthroughs must be respected
### * last block must remain the last block
def order_basic_blocks(blocks, succ, fallthrough_map):
  blockorder = []
  cur_block = None
  fallthroughs = fallthrough_map.values()
  while len(blockorder) < len(blocks):
    if cur_block is None:
      for blockname,_ in blocks.items():
        if blockname not in blockorder \
           and blockname not in fallthroughs \
           and (len(blockorder) != len(blocks) - 1 or len(succ[blockname]) == 0):
          cur_block = blockname
          break

    else:
      blockorder.append(cur_block)
      if cur_block in fallthrough_map:
        cur_block = fallthrough_map[cur_block]

      else:
        cur_block = None

  return blockorder


### rename jump targets
def rename_targets(target_map, instrs):
  new_instrs = []
  for instr in instrs:
    if "op" in instr and instr["op"] == "jmp":
      target = instr["args"][0]
      new_instr = {
        "op": "jmp",
        "args": [target_map[target] if target in target_map else target],
      }
      new_instrs.append(new_instr)

    elif "op" in instr and instr["op"] == "br":
      then_target = instr["args"][1]
      else_target = instr["args"][2]
      new_instr = {
        "op": "br",
        "args": [
          instr["args"][0], 
          target_map[then_target] if then_target in target_map else then_target,
          target_map[else_target] if else_target in target_map else else_target
        ]
      }
      new_instrs.append(new_instr)

    else:
      new_instrs.append(instr)

  return new_instrs


### convert block map into instructions, given a block order
def blockmap_to_instrs(blocks, blockorder, header_map, natloop_info):
  instrs = []
  natloop_headers = {}
  for preheader_name, info in natloop_info.items():
    natloop_headers[info["header_name"]] = info["natloop"]

  for blockname in blockorder:
    instrs.append({"label": blockname})
    # rename jump targets, except for when blocks are inside natural loops
    block_header_map = {}
    for header_name, natloop in natloop_headers.items():
      if blockname not in natloop:
        block_header_map[header_name] = header_map[header_name]

    block_instrs = rename_targets(block_header_map, blocks[blockname])
    instrs.extend(block_instrs)

  return instrs


### it's loop-invariant code motion, baby
def codemotion(instrs):
  # create CFG and dominator tree
  blocks = block_map(form_blocks(instrs))
  add_terminators(blocks)
  pred, succ = edges(blocks)
  domtree = get_dom(succ,list(blocks.keys())[0])
  
  # perform reaching definitions analysis
  rins, routs = reachers(blocks) # what is reaching
  rdef_var_ins  = reaching_def_vars(blocks, rins)
  rdef_var_outs = reaching_def_vars(blocks, routs)

  natloop_ind = 1
  natloop_info = {}
  for source,sink in get_backedges(succ, domtree):
    natloop = loopsy(source, sink, pred)

    # compute which instructions to hoist
    invmap = invloop(blocks, rdef_var_ins, rdef_var_outs, natloop) 
    hoistmap = hoistloop(blocks, succ, domtree, rdef_var_ins, rdef_var_outs, \
        natloop, invmap)

    preheader = build_preheader(blocks, natloop, hoistmap)
    natloop_blocks = hoist_instructions(blocks, natloop, hoistmap)

    preheader_name = "preheader" + str(natloop_ind)
    natloop_ind += 1
    # make sure preheader precedes header
    succ[preheader_name] = [sink]

    # save natural loop information
    natloop_info[preheader_name] = {
      "preheader": preheader,
      "header_name": sink,
      "natloop": natloop,
      "natloop_blocks": natloop_blocks
    }

  # generate new instructions
  new_blocks = dict(blocks)
  header_map = {}
  for preheader_name, info in natloop_info.items():
    header_map[info["header_name"]] = preheader_name
    if len(info["preheader"]) > 0:
      new_blocks[preheader_name] = info["preheader"]

    for blockname, block in info["natloop_blocks"].items():
      new_blocks[blockname] = block

  fallthrough_map = get_fallthroughs(new_blocks, succ)
  blockorder = order_basic_blocks(new_blocks, succ, fallthrough_map)
  new_instrs = blockmap_to_instrs(new_blocks, blockorder, header_map, natloop_info)
  return new_instrs


### perform code motion for all bril functions
def bril_codemotion(bril):
  new_funcs = []

>>>>>>> c04226ddf403fc9a006c79f8d078c825897d881c
  for func in bril['functions']:
    new_instrs = codemotion(func["instrs"])
    new_funcs.append({"instrs": new_instrs, "name": func["name"]})

  return {"functions": new_funcs}


if __name__ == '__main__':
    print(json.dumps(bril_codemotion(json.load(sys.stdin))))


### eof
