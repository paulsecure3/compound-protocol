certoraRun contracts/CErc20.sol contracts/Comptroller.sol contracts/governance/Comp.sol \
    --verify Comptroller:claimCompRules.spec \
    --solc solc5.17 \
    --optimistic_loop \
    --link Comptroller:_compAddress=Comp \
    --settings -copyLoopUnroll=4,-reachVarsFoldingBound=0,-postProcessCounterExamples=true,-t=600,-depth=14 \
    --cache compoundClaimCompRules \
    --staging --rule maxCompReward \
    --msg "compound claim comp rules - change msg"