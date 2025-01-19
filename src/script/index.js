import { exec } from 'child_process';
import chalk from 'chalk';

const APP_PATH = 'node_modules/.bin/app.exe';

const commands = [
  { args: '--help', expected: 'Available commands:' },
  { args: '--version', expected: '1.0.0' },
  { args: '--button1', expected: 'Button 1 clicked' },
  { args: '--button2', expected: 'Button 2 clicked' },
  { args: '--invalid', expected: 'Invalid command' },
];

const testCommand = (command) => {
  return new Promise((resolve, reject) => {
    exec(`${APP_PATH} ${command.args}`, (error, stdout, stderr) => {
      if (error) {
        console.error(
          chalk.red(`Error while running: ${command.args}\n${error.message}`)
        );
        return reject(error);
      }

      const output = stdout.trim();
      console.log(chalk.blue(`Testing: ${command.args}`));
      console.log(chalk.yellow(`Expected result: ${command.expected}`));
      console.log(chalk.green(`Actual result: ${output}`));

      if (output.includes(command.expected)) {
        console.log(chalk.green(`✓ Test ${command.args} passed\n`));
        resolve(true);
      } else {
        console.error(chalk.red(`✗ Test ${command.args} failed\n`));
        console.error(
          chalk.red(`Expected: ${command.expected}, Received: ${output}`)
        );
        resolve(false);
      }
    });
  });
};

(async () => {
  console.log(chalk.bold('Starting automated command tests...'));

  for (const command of commands) {
    try {
      await testCommand(command);
    } catch (error) {
      console.error(chalk.red(`Error during test: ${command.args}`));
    }
  }

  console.log(chalk.bold.green('\nAutomated command testing completed.'));
})();
