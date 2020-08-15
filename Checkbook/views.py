from django.shortcuts import render, redirect, get_object_or_404
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm


# Create your views here.
def home(request):
    form = TransactionForm(data=request.POST or None)
    if request.method == 'POST':
        pk = request.POST['account']
        return balance(request, pk)
    content = {'form': form}
    return render(request, 'checkbooktemps/index.html', content)


def create_account(request):
    form = AccountForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('index')
    content = {'form': form}
    return render(request, 'checkbooktemps/CreateNewAccount.html', content)


def balance(request, pk):
    account = get_object_or_404(Account, pk=pk)
    transactions = Transaction.Transactions.filter(account=pk)
    current_total = account.initial_deposit
    table_contents = {}
    for transaction in transactions:
        if transaction.type == 'Deposit':
            current_total += transaction.amount
            table_contents.update({transaction: current_total})
        else:
            current_total -= transaction.amount
            table_contents.update({transaction: current_total})

    content = {'account': account, 'table_contents': table_contents, 'balance': current_total}
    return render(request, 'checkbooktemps/BalanceSheet.html', content)


def transaction(request):
    form = TransactionForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            pk = request.POST['account']
            form.save()
            return balance(request, pk)

    content = {'form': form}
    return render(request, 'checkbooktemps/AddTransaction.html', content)
