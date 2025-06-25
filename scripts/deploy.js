const hre = require("hardhat");
const fs = require("fs");
const path = require("path");

async function main() {
  const [deployer] = await hre.ethers.getSigners();
  console.log("Deploying SpiralCooperative with guardian:", deployer.address);

  const SpiralCooperative = await hre.ethers.getContractFactory("SpiralCooperative");
  const contract = await SpiralCooperative.deploy([deployer.address]);

  await contract.waitForDeployment();
  const address = await contract.getAddress();

  console.log("SpiralCooperative deployed to:", address);

  // 🌀 Save to contract_info.json
  const artifact = await hre.artifacts.readArtifact("SpiralCooperative");
  const contractInfo = {
    address: address,
    abi: artifact.abi
  };

  const outputPath = path.join(__dirname, "../contract_info.json");
  fs.writeFileSync(outputPath, JSON.stringify(contractInfo, null, 2));
  console.log("Saved contract info to contract_info.json");
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
