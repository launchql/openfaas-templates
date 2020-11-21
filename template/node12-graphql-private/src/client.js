import env from './env';
import { GraphQLClient } from 'graphql-request';
export const client = new GraphQLClient(
  env.GRAPHQL_URL
);
export const jobsClient = new GraphQLClient(
  env.INTERNAL_JOBS_API_URL
);