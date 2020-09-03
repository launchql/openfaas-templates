import env from './env';
import { GraphQLClient } from 'graphql-request';
export const client = new GraphQLClient(
  env.GRAPHQL_URL
);