
 methods {
    function _.mintAllowed(address cToken, address minter, uint mintAmount) external => NONDET;
    function _.mintVerify(address cToken, address minter, uint mintAmount, uint mintTokens) external => NONDET;

    function _.redeemAllowed(address cToken, address redeemer, uint redeemTokens) external => NONDET;
    function _.redeemVerify(address cToken, address redeemer, uint redeemAmount, uint redeemTokens) external => NONDET;

    function _.borrowAllowed(address cToken, address borrower, uint borrowAmount) external => NONDET;
    function _.borrowVerify(address cToken, address borrower, uint borrowAmount) external => NONDET;

    function _.repayBorrowAllowed(
        address cToken,
        address payer,
        address borrower,
        uint repayAmount) external => NONDET;
    function _.repayBorrowVerify(
        address cToken,
        address payer,
        address borrower,
        uint repayAmount,
        uint borrowerIndex) external => NONDET;

    function _.liquidateBorrowAllowed(
        address cTokenBorrowed,
        address cTokenCollateral,
        address liquidator,
        address borrower,
        uint repayAmount) external => NONDET;
    function _.liquidateBorrowVerify(
        address cTokenBorrowed,
        address cTokenCollateral,
        address liquidator,
        address borrower,
        uint repayAmount,
        uint seizeTokens) external => NONDET;

    function _.seizeAllowed(
        address cTokenCollateral,
        address cTokenBorrowed,
        address liquidator,
        address borrower,
        uint seizeTokens) external => NONDET;
    function _.seizeVerify(
        address cTokenCollateral,
        address cTokenBorrowed,
        address liquidator,
        address borrower,
        uint seizeTokens) external => NONDET;

    function _.transferAllowed(address cToken, address src, address dst, uint transferTokens) external => NONDET;
    function _.transferVerify(address cToken, address src, address dst, uint transferTokens) external => NONDET;

    /*** Liquidity/Liquidation Calculations ***/

    function _.liquidateCalculateSeizeTokens(
        address cTokenBorrowed,
        address cTokenCollateral,
        uint repayAmount) external => NONDET;
}
