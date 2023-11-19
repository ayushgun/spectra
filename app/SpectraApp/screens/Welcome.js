import React, { memo } from 'react';
import Background from './components/Background';
import Logo from './components/Logo';
import Header from './components/Header';
import Paragraph from './components/Paragraph';
import Button from './components/Button';

const Welcome = ({navigation}) => (
  <Background>
    <Logo/>
    <Header>Vision for All</Header>
    <Paragraph>
      Navigate with confidence and detect dangers in your path.
    </Paragraph>
    <Button mode="outlined" onPress={() => navigation.navigate('Settings')}>
      Welcome to Spectra
    </Button>
  </Background>
);

export default Welcome;