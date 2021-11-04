using CERC20 as cToken
using COMP as comp

methods {
	comp.balanceOf(address user) returns uint envfree
	cToken.borrowBalanceStored(address borrower) returns uint envfree 
	cToken.balanceOf(address user) returns uint envfree 
}


/*
No COMP gain on borrow at zero block duration.
A user with zero borrows can not gain COMP instantly by using for example a flashloan.
*/
rule zeroGainOnZeroBlocks() {
	env e;
	address borrower;
	uint256 before = Comp.balanceOf(borrower);
	require cToken.borrowBalanceStored(borrower) == 0;
	cToken.borrow(e, borrowAmount);
	claimComp(borrower);
	uint256 after = Comp.balanceOf(borrower);
	assert before == after;
}


/*
No gain or loss of COMP tokens due to front-running. 
The amount of COMP received at a specific state is the same whether or not another user (possible admin) has performed an operation just before
*/
rule noGainDuetoOtherCall(method f) {
	env eUSer;
	env eOther;

	require eOther.block.timestamp < eUser.block.timestamp; 
	require eUser.msg.sender != eOther.msg.sender; 
	 
	storage init = lastStorage;
	claimComp(eUser);
	uint256 case1 = Comp.balanceOf(e.msg.sender);

	f(eOther,args) at init;
	claimComp(eUser);
	uint256 case2 = Comp.balanceOf(e.msg.sender);
	assert case1 == case2 ;
}

/* 
The max comp reward of a user has an upper limit, based on the current supplyState and borrowState
supply * ( getCompSupplierIndex(cToken) - compInitialIndex ) +  borrow * ( getCompBorrowState(cToken) - compInitialIndex ) 
*/
rule maxCompReward() {
	address user;
	uint compInitialIndex = compInitialIndex();
	uint256 before = Comp.balanceOf(user);
	uint256 supply = cToken.balanceOf(supplier);
	uint256 borrow = cToken.borrowBalanceStored(user);
	claimComp(e, user);
	uint256 after = Comp.balanceOf(user);
	mathint maxSupplyGain = supply * ( getCompSupplierIndex(cToken) - compInitialIndex );
	mathint maxBorrowGain = borrow * ( getCompBorrowState(cToken)  - compInitialIndex );

	assert after <= before + maxSupplyGain + maxBorrowGain;
}