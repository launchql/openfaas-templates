import { cleanEnv, port, url } from 'envalid';

export default cleanEnv(
  process.env,
  {
    GRAPHQL_URL: url(),
    INTERNAL_JOBS_API_URL: url(),
    PORT: port({ default: 10101 })
  },
  { dotEnvPath: null }
);
