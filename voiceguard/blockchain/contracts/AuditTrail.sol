// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title VoiceGuard AuditTrail Smart Contract
 * @dev Anchors cryptographic SHA-256 hash-chain batch roots on Ethereum compatible blockchains.
 */
contract AuditTrail {
    struct AuditRecord {
        uint256 batchIndex;
        bytes32 merkleRoot;
        uint256 eventCount;
        uint256 timestamp;
        address submitter;
    }

    address public owner;
    uint256 public totalBatches;
    mapping(uint256 => AuditRecord) public batchRecords;

    event BatchAnchored(
        uint256 indexed batchIndex,
        bytes32 indexed merkleRoot,
        uint256 eventCount,
        uint256 timestamp,
        address submitter
    );

    modifier onlyOwner() {
        require(msg.sender == owner, "VoiceGuard: Caller is not contract owner");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function anchorBatch(bytes32 merkleRoot, uint256 eventCount) external onlyOwner returns (uint256) {
        totalBatches++;
        
        batchRecords[totalBatches] = AuditRecord({
            batchIndex: totalBatches,
            merkleRoot: merkleRoot,
            eventCount: eventCount,
            timestamp: block.timestamp,
            submitter: msg.sender
        });

        emit BatchAnchored(totalBatches, merkleRoot, eventCount, block.timestamp, msg.sender);
        return totalBatches;
    }

    function verifyBatch(uint256 batchIndex, bytes32 merkleRoot) external view returns (bool) {
        if (batchIndex == 0 || batchIndex > totalBatches) {
            return false;
        }
        return batchRecords[batchIndex].merkleRoot == merkleRoot;
    }
}
