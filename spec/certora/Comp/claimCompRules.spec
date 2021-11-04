
using CErc20 as cToken
using Comp as comp

methods {
    comp.balanceOf(address user) returns uint envfree
    cToken.borrowBalanceStored(address borrower) returns uint envfree
    cToken.balanceOf(address user) returns uint envfree 
    getCompSupplierIndex(address) returns uint envfree
    getCompBorrowState(address) returns uint envfree
    getCompBorrowStateBlock(address) returns uint envfree
    getCompSupplierIndexBlock(address) returns uint envfree
    compAccrued(address) returns uint envfree
    compInitialIndex() returns uint224 envfree
    compSupplierIndex(address,address) returns uint envfree
    compBorrowerIndex(address,address) returns uint envfree
    assumeMarketWithOneCtoken(address) envfree
    balanceOf(address) => DISPATCHER(true)
    totalSupply() => DISPATCHER(true)
    borrowBalanceStored(address borrower) => DISPATCHER(true)
    borrowIndex() => DISPATCHER(true)
}

/*
No COMP gain on borrow at zero block duration.
A user with zero borrows can not gain COMP instantly by using for example a flashloan.
*/
rule zeroGainOnZeroBlocks() {
    env e;
    env e2;
    address borrower;
    uint256 before = comp.balanceOf(borrower);
    require cToken.borrowBalanceStored(borrower) == 0;
    uint borrowAmount;
    cToken.borrow(e, borrowAmount);
    claimComp(e2, borrower);
    uint256 after = comp.balanceOf(borrower);
    assert before == after;
}

/*
No gain or loss of COMP tokens due to front-running. 
The amount of COMP received at a specific state is the same whether or not another user (possible admin) has performed an operation just before
*/
rule noFrontRunningGainOrLose(method f) {
    env eUser;
    env eOther;

    require eOther.block.timestamp < eUser.block.timestamp; 
    require eUser.msg.sender != eOther.msg.sender; 
     
    storage init = lastStorage;
    claimComp(eUser, eUser.msg.sender);
    uint256 case1 = comp.balanceOf(eUser.msg.sender);
    calldataarg args;
    f(eOther,args) at init;
    claimComp(eUser, eUser.msg.sender);
    uint256 case2 = comp.balanceOf(eUser.msg.sender);
    assert case1 == case2;
}


/* The max comp reward of a user has an upper limit, based on the current SupplyState and borrowState and compAccured 
    supply * ( getCompSupplierIndex(cToken) - compInitialIndex ) +  borrow * ( getCompBorrowState(cToken) - compInitialIndex ) 
*/
/*
{ b = comp.balanceOf(user) }
    claimComp(e, user);
{ comp.balanceOf(user) <= before + maxSupplyGain + maxBorrowGain + compAccured[user]}
*/
rule maxCompReward() {
    address user;
    env e;

    // valid state and assumptions
    assumeMarketWithOneCtoken(cToken);
    uint256 compInitialIndex = to_uint256(compInitialIndex());
    require getCompSupplierIndex(cToken) >= compInitialIndex; 
    require getCompBorrowState(cToken)  >= compInitialIndex;
    require getCompBorrowStateBlock(cToken) == e.block.number;
    require getCompSupplierIndexBlock(cToken) == e.block.number;
    require compSupplierIndex(cToken,user) == 0 || compSupplierIndex(cToken,user) >= compInitialIndex;
    require compBorrowerIndex(cToken,user) == 0 || compBorrowerIndex(cToken,user) >= compInitialIndex;


    uint256 before = comp.balanceOf(user);
    uint256 supply = cToken.balanceOf(user);
    uint256 borrow = cToken.borrowBalanceStored(user);
    uint256 leftCompToClaim = compAccrued(user);
    claimComp(e, user);
    uint256 after = comp.balanceOf(user);
    mathint maxSupplyGain = supply * ( getCompSupplierIndex(cToken) - compInitialIndex );
    mathint maxBorrowGain = borrow * ( getCompBorrowState(cToken)  - compInitialIndex );
    assert  after <= before + maxSupplyGain + maxBorrowGain + leftCompToClaim;
}
    
