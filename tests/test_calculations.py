# import pytest
# from app.calculations import (
#     add,
#     subtract,
#     multiply,
#     divide,
#     BankAccount,
#     InsufficientFunds,
# )


# @pytest.fixture
# def zero_bank_account():
#     return BankAccount()


# @pytest.fixture
# def bank_account():
#     return BankAccount(50)


# @pytest.mark.parametrize("num1, num2, expected", [(3, 1, 4), (5, 9, 14), (6, 7, 13)])
# def test_add(num1, num2, expected):
#     print("testing add function")
#     assert add(num1, num2) == expected


# def test_subtract():
#     assert subtract(9, 4) == 5


# def test_multiply():
#     assert multiply(5, 3) == 15


# def test_divide():
#     assert divide(4, 2) == 2


# def test_bank_set_initial_amount(bank_account):
#     assert bank_account.balance == 50


# def test_default_bank_amount(zero_bank_account):
#     assert zero_bank_account.balance == 0


# def test_withdraw(bank_account):

#     bank_account.withdraw(4)
#     assert bank_account.balance == 46


# def test_deposit(bank_account):
#     bank_account.deposit(10)
#     assert bank_account.balance == 60


# def test_interest(bank_account):
#     bank_account.collect_interest()
#     assert round(bank_account.balance) == 55


# @pytest.mark.parametrize(
#     "deposited, withdrew, expected_amount",
#     [(200, 100, 100), (50, 10, 40), (500, 20, 480)],
# )
# def test_bank_transaction(zero_bank_account, deposited, withdrew, expected_amount):
#     zero_bank_account.deposit(deposited)
#     zero_bank_account.withdraw(withdrew)
#     assert zero_bank_account.balance == expected_amount


# def test_insufficient_funds(bank_account):
#     with pytest.raises(InsufficientFunds):
#         bank_account.withdraw(200)
