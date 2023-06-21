import "erc20.spec";
import "comptroller.spec";

using DummyERC20A as underlying;

methods {
	// assume accure has been called already 
	function accrueInterest() internal returns (uint256) => NONDET;

	// envfree methods
	function getCash() external returns (uint256) envfree;
	function totalSupply() external returns (uint256) envfree;
	function balanceOf(address) external returns (uint256) envfree;

	// underlying erc20 
	function DummyERC20A.balanceOf(address) external returns (uint256) envfree;
}

rule sanity(method f)
{
	env e;
	calldataarg args;
	f(e,args);
	assert false;
}

invariant supplyImpliesCash() 
	totalSupply() == 0 <=> getCash()==0 ;


rule dustFavorsTheHouse() {
	env e;
	uint256 mintAmount;

	uint256 systemCashBefore = getCash();
	uint256 userCtokenBefore = balanceOf(e.msg.sender);
	mint(e, mintAmount);
	uint256 userCtokenAfter = balanceOf(e.msg.sender);
	mathint receivedCToken = userCtokenAfter - userCtokenBefore;
	redeem(e,assert_uint256(receivedCToken));

	assert getCash() >= systemCashBefore;
}