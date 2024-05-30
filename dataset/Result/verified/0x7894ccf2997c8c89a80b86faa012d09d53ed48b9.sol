/**
 *Submitted for verification at Etherscan.io on 2016-04-03
*/

contract thesimplegame {

  struct Person {
      address etherAddress;
      uint amount;
  }

  Person[] public persons;

  uint public payoutIdx = 0;
  uint public collectedFees;
  uint public balance = 0;

  address public owner;


  modifier onlyowner { if (msg.sender == owner) _ }


  function thesimplegame() {
    owner = msg.sender;
  }

  function() {
    enter();
  }
  
  function enter() {
    if (msg.value < 1/100 ether) {
        msg.sender.send(msg.value);
        return;
    }
	
		uint amount;
		if (msg.value > 10 ether) {
			msg.sender.send(msg.value - 10 ether);	
			amount = 10 ether;
    }
		else {
			amount = msg.value;
		}


    uint idx = persons.length;
    persons.length += 1;
    persons[idx].etherAddress = msg.sender;
    persons[idx].amount = amount;
 
    
    if (idx != 0) {
      collectedFees += amount / 10;
	  owner.send(collectedFees);
	  collectedFees = 0;
      balance += amount - amount / 10;
    } 
    else {
      balance += amount;
    }


    while (balance > persons[payoutIdx].amount / 100 * 125) {
      uint transactionAmount = persons[payoutIdx].amount / 100 * 125;
      persons[payoutIdx].etherAddress.send(transactionAmount);

      balance -= transactionAmount;
      payoutIdx += 1;
    }
  }


  function setOwner(address _owner) onlyowner {
      owner = _owner;
  }
}