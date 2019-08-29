pragma solidity >=0.5.0 <0.6.0;
pragma experimental ABIEncoderV2;

import "./rlp-decode.sol";

contract LightClientArbiter {
    
    using RLPDecode for bytes;
    using RLPDecode for uint;
    using RLPDecode for RLPDecode.RLPItem;

    event Bytes32(string msg, bytes32 b);
    event Bytes(string msg, bytes h);
    event Bool(string msg, bool b);
    event BytesArray(string msg, bytes[] ba);
    event UintArray(string msg, uint256[] uia);
    
    mapping (uint256 => bytes32) public blockhashes;
    mapping (address => uint256) public deposits;
    
    mapping (address => uint256) public honesties;
    mapping (address => bool) public provables;
    
    address public lwn;
    address public rfn1;
    address public rfn2;
    
    uint256 public k;
    uint256 public r;
    uint256 public df;
    uint256 public dl;
    
    uint public state;
    bytes32 public queried_tx_hash;
    
    bytes32 public bottomHash = 0x1dea6b9299e3150ba010c70180916ae71d92825cf44462aabbed0ec45bf64aaa;
    
    struct existenceProof {
        bytes rlpHeader;
        bytes32 txHash;
        bytes[] rlpTrieNodes;
        uint256[] trieKeys;
    }
    
    struct signature {
        uint8 v;
        bytes32 r;
        bytes32 s;
    }
    
    constructor() public {
        blockhashes[8426062] = 0xbb41784f87f501da25af08513aa3267524c063037268b59751b7b69b4d65e390; //0x0661d6e95ab1320e93165c37b0e666c96c97b49a8819c02a8cda05c38ff5a97d
        blockhashes[8290728] = 0xcb818dc8816bef7f0690dda4cdd7d1cc50c807310132aa337a35bb5a46438024; //0x14198912703598b497ffbe17e6a90ffa85de276418ae41d217c0e3d2c76290d7
        blockhashes[8429602] = 0x1dfc2529a67c863062b434d7cba71eb921884c388ba96183f2a7c64c8d1753b9; //0x949ae094deb031cbcfb1aaf36ca62b49d5e1d34affbbda16f7323568d8ac2689
        blockhashes[8429146] = 0xa036bb158e21d9aae09faa82860ff522bdc5dff5187dc857561f5fa4d5596bb7; //0x1e39d5b4b46d420e960e12ba2544988bc11c4d4e8c12ceca4871d306afd73d44
        blockhashes[8437201] = 0x5d61b7f62528549ee7f9d170d345e7cb1a6dee11384d22a35a67011895ef7b90; //0xfe28a4dffb8ece2337863fba8dfd2686e9a9c995b50fe7911acbb2589f80b315
        // lwn = 0x802Fd9c8369AF656196547d3619aEF222bE56777;
        lwn = 0xCA35b7d915458EF540aDe6068dFe2F44E8fa733c;
        rfn1 = 0x3ca68896d4111E26847100C5328fF4F3F3b31B84;
        rfn2 = 0xd5F4538211bf0F6cCb3c7a7934768E7E2B5703f2;
        state = 1;
        k = 5;
        r = 50;
        df = 200;
        dl = 100;
        deposits[lwn] = dl;
        deposits[rfn1] = k * df;
        deposits[rfn2] = k * df;
    }
    
//0x14198912703598b497ffbe17e6a90ffa85de276418ae41d217c0e3d2c76290d7
    function request(bytes32 txHash) public {
        assert (msg.sender == lwn && state == 1 && k > 0);
        honesties[rfn1] = 0;
        honesties[rfn2] = 0;
        provables[rfn1] = false;
        provables[rfn2] = false;
        state = 2;
        queried_tx_hash = txHash;
    }


//[["0xf90215a0601e48a9ec198e0fa3c8130bd088397eb25c8f2143ba0ceab776c0530eaa5ffaa01dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d4934794829bd824b016326a401d083b33d092293333a830a09e10d56ddb125062b5ce43de1b022772cb5cec2c382741832187a92fc692db65a0dc8c85010ffbcc62e70cb0b172a600895550409972241d4b9487e4767a5ec7aaa0d64a31c3b11d9725b612b6baca331f3e6b9243fdd105eae633b8e1d6337f1ce4b901000000000000000020000000000000000400000000000000080001800000000000000000000008004000100000000000000000040000000001000000000000000000000000000000004000000800000000000040000000000002000000000000000000000008000004000000000000001000001000000000000000001000200000000000000000000000040000900000000000110000000000000000000000000000000000000000000000000000000000004000000000000000000000100000000000000200000000000000000000000000040000000040000000000800000000000040000100002000000000000000000000200000000000000000000000000887082c3f019b1ecf837e81a8837a308383042bba845d4825ba947070796520e4b883e5bda9e7a59ee4bb99e9b1bca07eed785f1d2e89eea2ca06f2f8bc46869b77c8575cc02f6c2b00ca19bc71607988a14db2500204bfd3", "0x14198912703598b497ffbe17e6a90ffa85de276418ae41d217c0e3d2c76290d7",["0xf851a0a562f8ade1bdb49e380246162ac1002f33621ace67bc062afaf952154233463780808080808080a051b75bd5a95e582e973418e878473a7cc2ce2a98c9495f0a033f83a57f0ded038080808080808080","0xf8d180a0e9afd1a676944917863edc8bef035f5d30abba7114a1086c944aaf50350617fea0114b92df52bd35e79ec702f0c4c17c1ba0273e98c9a5b81003fb21bdb09ffcd8a0848f1f5d46522ef2364565df33a090b42d7f42282df087f97d78eae384e28c01a05355924d0df1cea27e8966a9ee96d1c431a20d5709acc73a77852b312a340fa0a0588050f1495db6cbaf4d60b40c1d44b2ca0d7c8778847acdf002c5e9be341b3ba09205adaf20ccd4e495580b1a0ad96007f59fff4e16e0858f6144f91cda9d753680808080808080808080", "0xf87120b86ef86c028502540be400825208941b9c9c55039898417df74998e00474ae62a2405b880f44bb2a745520008026a091426cf2529c5653d2dd7085571aa45be7dd25e35b6cc70fec865f5d54966330a05a2577d3b93cd6a4cde5385fc3cdb3160e04eb8ebc703bd0fbd969c8216b2136"],[0,3,1]]]
//[[28, "0xa27164e3c1a78b182444e3cd305443581362458cc6beb30c9974dbfcda6332e8", "0x1d07fbd154c0e39357590efad43c386b387c8e9450cd0bf0a30617b6c4f1a6fc"]]
//[0]
    function feedback(existenceProof[] memory proofs, signature[] memory sigs, bool[] memory opt_modes) public {
        assert (msg.sender == lwn && state == 2);
        assert (proofs.length == sigs.length && opt_modes.length == sigs.length);
        assert (sigs.length == 1 || sigs.length == 2);
        
        uint256 num = sigs.length;
        
        if (num == 1) {
            //address addr = verifyForwardedExistenceProof(proofs[0], sigs[0]);
            assert(queried_tx_hash == proofs[0].txHash);
            bytes32 digest = keccak256(abi.encode(proofs[0].rlpHeader, proofs[0].txHash, proofs[0].rlpTrieNodes, proofs[0].trieKeys));
            address addr = verifySig(digest, sigs[0].v, sigs[0].r, sigs[0].s);
            assert (addr == rfn1 || addr == rfn2);
            if (digest == bottomHash) {
                honesties[addr] = 1;
            } else {
                bytes memory rootHash = getTrieRootHash(proofs[0].rlpHeader); 
                if (verifyTrieProof(rootHash, proofs[0].txHash, proofs[0].rlpTrieNodes, proofs[0].trieKeys)) {
                    honesties[addr] = 1;
                }
            }
        }
        
        if (num == 2) {
            //address addr1 = verifyForwardedExistenceProof(proofs[0], sigs[0]);
            //address addr2 = verifyForwardedExistenceProof(proofs[1], sigs[1]);
            assert(queried_tx_hash == proofs[0].txHash);
            assert(queried_tx_hash == proofs[1].txHash);
            bytes32 digest1 = keccak256(abi.encode(proofs[0].rlpHeader, proofs[0].txHash, proofs[0].rlpTrieNodes, proofs[0].trieKeys));
            address addr1 = verifySig(digest1, sigs[0].v, sigs[0].r, sigs[0].s);
            bytes32 digest2 = keccak256(abi.encode(proofs[1].rlpHeader, proofs[1].txHash, proofs[1].rlpTrieNodes, proofs[1].trieKeys));
            address addr2 = verifySig(digest2, sigs[1].v, sigs[1].r, sigs[1].s);
            assert (addr1 == rfn1 && addr1 == rfn2);
            if (digest1 == bottomHash && digest2 == bottomHash) {
                honesties[addr1] = 1;
                honesties[addr2] = 1;
            } else if (digest1 == bottomHash && digest2 != bottomHash) {
                bytes memory rootHash2 = getTrieRootHash(proofs[1].rlpHeader); 
                if (verifyTrieProof(rootHash2, proofs[1].txHash, proofs[1].rlpTrieNodes, proofs[1].trieKeys)) {
                    honesties[addr1] = 0;
                    honesties[addr2] = 2;
                } else {
                    honesties[addr1] = 1;
                }
            } else if (digest1 != bottomHash && digest2 == bottomHash) {
                 bytes memory rootHash1 = getTrieRootHash(proofs[0].rlpHeader); 
                 if (verifyTrieProof(rootHash1, proofs[0].txHash, proofs[0].rlpTrieNodes, proofs[0].trieKeys)) {
                     honesties[addr1] = 2;
                     honesties[addr2] = 0;
                 } else {
                     honesties[addr2] = 1;
                 }
            } else {
                bytes memory rootHash1 = getTrieRootHash(proofs[0].rlpHeader); 
                bytes memory rootHash2 = getTrieRootHash(proofs[1].rlpHeader); 
                if (verifyTrieProof(rootHash1, proofs[0].txHash, proofs[0].rlpTrieNodes, proofs[0].trieKeys)) {
                    honesties[addr1] = 1;
                }
                if (verifyTrieProof(rootHash2, proofs[1].txHash, proofs[1].rlpTrieNodes, proofs[1].trieKeys)) {
                    honesties[addr2] = 1;
                }
                if (honesties[addr1] == 1 && honesties[addr2] == 0) {
                    honesties[addr1] = 2;
                } else if (honesties[addr1] == 0 && honesties[addr2] == 1) {
                    honesties[addr2] = 2;
                }
            }
        }
        state = 1;
        k = k - 1;
        if (k == 0) {
            state = 3;
        }
    }
    
    function kill() public payable {
        assert (state == 3);
        assert (msg.sender == lwn);
        selfdestruct(msg.sender);
    }
    
// Test case 1:
//["0xf90217a07d7c5a485f7832e1ca25b769354f9d261d35fb02b69fd2a48def02506d7ee775a01dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d4934794ea674fdde714fd979de3edf0f56aa9716b898ec8a026f417f798d9c3d1076b030220ed71fbed077375b8ee400a71fc7b75d9d60d38a0404e40fa33188ef3a5226eaa973bfa88544876727b99465da862c9f86329f826a0241e5e8cc958c4115e3459be1fb211b5e8c2683fd58bcbb86fe9aee9cd307784b90100924120844c00a4c202832a106404898120204060202860681424c4044702424040105458e5d4428c718c09088a240541416a45923320cc054421671083313042a065b000a242850d0820800810824400c7102c008e22820080106a60534192d498018085018092449d305c981488004101329400a002c48904803310685078031483905c26042c8105c001148505010200490cb355a00a15c9494a20f291422006aa61a00d00f084a4b42cb000009224020a10c00885113c2d0b6028986c260808900d628000013b869bc361041a80082000ac980088c8340c000240001ca481831814097d000313390130941c9cb08090054a00002000dc6001f00724940e208707c6f2645ee2828380a022837a21288378cfe4845d64985696505059452d65746865726d696e652d61736961312d34a056fdf85c11b927850a5d204a4f269130e87815fa378a8cb942e793cb6638f6f2881eda81053e24d05d", "0x949ae094deb031cbcfb1aaf36ca62b49d5e1d34affbbda16f7323568d8ac2689", ["0xf90131a062e9398db032dd6c401390db73bb813cf669f238ecaff0b0066da02fc0ff10dba01c4eac69fd693b6c3b679240e855bb965d8508c5abaf619be147da57d5efeb8da0222e0d2ee97be6c3292b212a7f6a9fe67a48b7d21a46cdb8ffe073dc8cfd42a1a0b1f16b2c30108af0225e36349131fd01d87f656ddf7165b9019c029233cce0d5a0ee0febd8e78edb42f24e73b50a4ae0fb052c33cb00191446425ea5a9c54c8199a0947e91bfd29e751ac04bbe47e97dc550ff8942fd634c5d7553182239ef512f9ba07f6c2af9e6dbd9db8df205ade0e18c10ee9c0802705272399aab2bc0aea2c294a02505d0b053067263b15bdc0e32747371b91ebe23bc11916989fa07e6f60a6bcda0e58e97441710b910ec3513abd26b121fda8d5e3e7263ed585aa4ff4dcf73bd618080808080808080", "0xf90211a0f4cb7618a10aec7f3a3f5a320b6be17d673f806f603f284c836dec89c8f531fba022d2e743581468ab667b1ca577a6834804dc5f22bf15813847e94af339993f5ca04b7cb7fc67733ac9ff05e6f39652d6f1e93ced7663070a0a7232a3b015f9be68a0025cbb84cc076fc421b475dcf3fc1c83b3518d411ea98f5cdfe85beb094d3617a042e4a060bb4c4b9ab3eb1e8b81af54d904e2ba9f3b64feb54165fcbbff08838ca0e953bce4ba7b89e6090fb1f4291a7ec12c5a00ce7abceae1fd6de1540e570192a028905022e61f08fa8659b03df5220a6fcef3d54b5c16130f94beb864f07d1258a0508f7e3fa37e630171b3a1a13940488e55d3ca848b1948157b0774aba6c8f175a0045fd349e5f52b419740eb3c2c7c8144f12006e7f6290284143609df145152b4a09032ea9e4a5a68aa462f441b526c619c98887b2ebcd1f2702a1a155d105f6ac0a0892b152f88f6a75fa40241d18735c551e9030efae2e519f2e6425632dbb03f8fa059eda0988dd71d556be03be73452219c4b9b0d723bb856fc4977d6eef129186ba046d1a4b86e6c50bbd057786ee3085bcf6ce1d2e0500b08f03a591032f6180725a00c704e7e45f878942010685ca67477bd8ebadf51d787c3c7095f7452e149ca32a034c7fe56e0bd3d721532f82a4af59c8019e8b27b79cf3cd06d78c02ab1f914d2a09bd758d90cb4274a2a46c8ffcebde6dddc0074dacac9504328f655faee92016180", "0xf87420b871f86f8247c485051f4d5c0083015f9094517dd472d86c0388b71a5d31c2c509d3ea97f836888ab55f8b520780008026a011dc6365cf58c966c795765b495417664d23010dc30157b598a318e4cc550c20a06dda036a5b35ebd6edf20e092fb945ff5e28d1ddf09c74a32d03f51ef4e761b9"], [4, 14, 1]]    // [28, "0xa27164e3c1a78b182444e3cd305443581362458cc6beb30c9974dbfcda6332e8", "0x1d07fbd154c0e39357590efad43c386b387c8e9450cd0bf0a30617b6c4f1a6fc"]
//[28, "0xa27164e3c1a78b182444e3cd305443581362458cc6beb30c9974dbfcda6332e8", "0x1d07fbd154c0e39357590efad43c386b387c8e9450cd0bf0a30617b6c4f1a6fc"]

    function verifyTrieProof(bytes memory rootHash, bytes32 txHash, bytes[] memory rlpTrieNodes, uint256[] memory keys) pure internal returns (bool) {
        bytes memory nodeHash = rootHash;
        if (rlpTrieNodes.length != keys.length) {
            return false;
        }
        uint i = 0;
        while (i < rlpTrieNodes.length - 1) {
            if (bytesToBytes32(nodeHash) != keccak256(rlpTrieNodes[i])) {
                return false;
            }
            nodeHash = decodeRlpTrieNode(rlpTrieNodes[i])[keys[i]];
            i = i + 1;
        }
        if (bytesToBytes32(nodeHash) != keccak256(rlpTrieNodes[i])) {
            return false;
        }
        bytes memory tx_rlp = decodeRlpTrieNode(rlpTrieNodes[i])[keys[i]];
        if (txHash != keccak256(tx_rlp)) {
            return false;
        }
        return true;
    }
    
    function decodeRlpTrieNode(bytes memory item) internal pure returns (bytes[] memory) {
        RLPDecode.RLPItem[] memory items = item.toRlpItem().toList();
        bytes[] memory bytes_itmes = new bytes[](items.length);
        for (uint i = 0; i < items.length; i++) {
            bytes_itmes[i] = items[i].toBytes();
        }
        return bytes_itmes;
    }
    
    function getTrieRootHash(bytes memory rlpHeader) internal view returns (bytes memory) {
        return decodeRlpBlockHeader(rlpHeader);
    }
  
    function decodeRlpBlockHeader(bytes memory item) internal view returns (bytes memory) {
        RLPDecode.RLPItem[] memory items = item.toRlpItem().toList();
        if (blockhashes[items[8].toUint()] != keccak256(item)) {
            bytes memory zero = "0x0";
            return zero;
        }
        return items[4].toBytes();
    }
    
    function bytesToBytes32(bytes memory  _input) internal pure returns (bytes32) {
        bytes32 result;
        assembly {
            result := mload(add(_input, 32))
        }
        return result;
    }
    
    function verifySig(bytes32 _digest, uint8 _v, bytes32 _r, bytes32 _s) internal pure returns (address) {
        address signer = ecrecover(_digest, _v, _r, _s);
        return signer;
    }
    
}
