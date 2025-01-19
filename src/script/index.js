import chalk from 'chalk';
import path from 'path';
import { exec } from 'child_process';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';

dotenv.config();

const currentDir = path.dirname(fileURLToPath(import.meta.url));
const APP_PATH = path.join(currentDir, '..', '..', 'main.exe');

const helpExpected = [
  'button1: Get IPv4 Info',
  'button2: Check Proxy',
  'button3: System Info',
  'button4: BIOS Version',
  'button5: Host Name',
].join('\n');

const commands = [
  { args: 'help', expected: helpExpected },
  { args: 'button1', expected: process.env.BUTTON1_EXPECTED },
  { args: 'button2', expected: process.env.BUTTON2_EXPECTED },
  { args: 'button3', expected: process.env.BUTTON3_EXPECTED },
  { args: 'button4', expected: process.env.BUTTON4_EXPECTED },
  { args: 'button5', expected: process.env.BUTTON5_EXPECTED },
  {
    args: 'invalid',
    expected: "Invalid command. Use 'help' for a list of commands.",
  },
];

function normalize(str) {
  return str
    .replace(/\r\n/g, '\n')
    .replace(/\r/g, '\n')
    .replace(/\n/g, ' ')
    .trim();
}

const testCommand = (command) => {
  return new Promise((resolve, reject) => {
    exec(`${APP_PATH} ${command.args}`, (error, stdout) => {
      if (error) {
        console.error(
          chalk.red(`Error while running: ${command.args}\n${error.message}`)
        );
        return reject(error);
      }

      const output = stdout;
      console.log(chalk.blue(`\nTesting: ${command.args}`));
      console.log(chalk.yellow(`Expected result:\n${command.expected}`));
      console.log(chalk.green(`Actual result:\n${output}`));

      if (normalize(output) === normalize(command.expected)) {
        console.log(chalk.green(`✓ Test ${command.args} passed`));
        resolve(true);
      } else {
        console.error(chalk.red(`✗ Test ${command.args} failed`));
        resolve(false);
      }
    });
  });
};

(async () => {
  console.log(chalk.bold('Starting automated command tests...'));

  let passedTests = 0;
  const totalTests = commands.length;

  for (const command of commands) {
    try {
      const result = await testCommand(command);
      if (result) {
        passedTests += 1;
      }
    } catch (error) {
      console.error(chalk.red(`Error during test: ${command.args}`));
    }
  }

  console.log(
    chalk.bold.green(
      `\nAutomated command testing completed. ${passedTests}/${totalTests} tests passed.`
    )
  );
})();
