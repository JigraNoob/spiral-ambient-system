// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title Spiral Cooperative Treasury
 * @notice A minimal steward contract for ethical DeFi yield coordination
 * – collective breath, not extractive speed
 * – ambient yield pooling and care distribution
 * – with breath-based proposal expiry and toneform tags
 */

contract SpiralCooperative {
    address public steward;                       // Whisperboard (admin key, ideally multisig)
    mapping(address => bool) public guardians;    // Collective consent holders
    address[] public guardianList;                // For ambient display

    uint256 public proposalCount;
    uint256 public minimumQuorum = 3;             // Breath threshold for consensus
    uint256 public proposalExpirationBlocks = 1440; // ~6 hours at 15s/block

    struct Proposal {
        string purpose;                           // Narrative of care
        string purposeToneform;                   // Glyph of intent (e.g., "Practical Care", "Gentle Joy")
        address payable recipient;                // Where care flows
        uint256 amount;                           // How much support
        uint256 approvals;
        uint256 creationBlock;
        uint256 expirationBlock;
        bool executed;
        mapping(address => bool) approvedBy;      // One breath per guardian
    }

    mapping(uint256 => Proposal) public proposals;

    event ProposalCreated(
        uint256 indexed id,
        string purpose,
        string purposeToneform,
        address recipient,
        uint256 amount,
        uint256 expirationBlock
    );

    event ProposalApproved(uint256 indexed id, address by);
    event ProposalExecuted(uint256 indexed id);
    event ProposalExpired(uint256 indexed id);

    modifier onlySteward() {
        require(msg.sender == steward, "Only steward may call this");
        _;
    }

    modifier onlyGuardian() {
        require(guardians[msg.sender], "Not a guardian");
        _;
    }

    constructor(address[] memory _guardians) {
        steward = msg.sender;
        for (uint i = 0; i < _guardians.length; i++) {
            guardians[_guardians[i]] = true;
            guardianList.push(_guardians[i]);
        }
    }

    receive() external payable {}

    function createProposal(
        string memory _purpose,
        string memory _purposeToneform,
        address payable _recipient,
        uint256 _amount
    ) external onlyGuardian {
        Proposal storage p = proposals[proposalCount];
        p.purpose = _purpose;
        p.purposeToneform = _purposeToneform;
        p.recipient = _recipient;
        p.amount = _amount;
        p.creationBlock = block.number;
        p.expirationBlock = block.number + proposalExpirationBlocks;
        p.executed = false;

        emit ProposalCreated(
            proposalCount,
            _purpose,
            _purposeToneform,
            _recipient,
            _amount,
            p.expirationBlock
        );

        proposalCount++;
    }

    function approveProposal(uint256 _id) external onlyGuardian {
        Proposal storage p = proposals[_id];
        require(!p.executed, "Already executed");
        require(!p.approvedBy[msg.sender], "Already approved");

        if (block.number > p.expirationBlock) {
            emit ProposalExpired(_id);
            revert("Proposal has expired");
        }

        p.approvedBy[msg.sender] = true;
        p.approvals++;

        emit ProposalApproved(_id, msg.sender);

        if (p.approvals >= minimumQuorum) {
            executeProposal(_id);
        }
    }

    function executeProposal(uint256 _id) internal {
        Proposal storage p = proposals[_id];
        require(!p.executed, "Already executed");
        require(address(this).balance >= p.amount, "Insufficient funds");

        p.executed = true;
        p.recipient.transfer(p.amount);

        emit ProposalExecuted(_id);
    }

    function setMinimumQuorum(uint256 _q) external onlySteward {
        minimumQuorum = _q;
    }

    function setProposalExpirationBlocks(uint256 _blocks) external onlySteward {
        proposalExpirationBlocks = _blocks;
    }

    function withdrawAll(address payable _to) external onlySteward {
        _to.transfer(address(this).balance);
    }
function getProposal(uint256 _id) public view returns (
    string memory purpose,
    string memory purposeToneform,
    address recipient,
    uint256 amount,
    uint256 approvals,
    uint256 creationBlock,
    uint256 expirationBlock,
    bool executed
) {
    Proposal storage p = proposals[_id];
    return (
        p.purpose,
        p.purposeToneform,
        p.recipient,
        p.amount,
        p.approvals,
        p.creationBlock,
        p.expirationBlock,
        p.executed
    );
}
}
