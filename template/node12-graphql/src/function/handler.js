import gql from 'graphql-tag';
import fetch from 'cross-fetch';

// example GQL 
const GetUsers = gql`
  query GetUsers {
    users {
      nodes {
        id
        username
      }
    }
  }
`;

export default async (params, context) => {
  const { client } = context;
  // example request
  const github = await fetch('https://api.github.com/users/pyramation');
  // example query
  const apiInfo = await client.request(GetUsers);

  // return whatever you want
  return {
    works: true,
    apiInfo,
    github,
    ...params
  };
};
