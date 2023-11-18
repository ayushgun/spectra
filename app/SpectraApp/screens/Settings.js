import React, { memo } from 'react';
import Background from './components/Background';
import TextInput from './components/TextInput';
import Header from './components/Header';
import Paragraph from './components/Paragraph';
import Button from './components/Button';
import { SafeAreaView, StyleSheet } from 'react-native';
import { SegmentedButtons } from 'react-native-paper';
import { theme } from './core/theme';

const Welcome = ({navigation}) => {

    const [value, setValue] = React.useState('');
    const [email, setEmail] = React.useState('');

return (

  <Background>
    <Header>Action Phrase</Header>
    <Paragraph>
      Set your action phrase to activate Spectra.
    </Paragraph>
    <TextInput
    value={email.valueOf()}
    onChangeText={text => setEmail({ value: text, error: '' })}
    />

    <Header>Voice Style</Header>
    <Paragraph>
      Choose a voice style for Spectra.
    </Paragraph>
      <SegmentedButtons style={styles.SegmentedButtons}
        value={value}
        onValueChange={setValue}
        buttons={[
          {
            value: 'male',
            label: 'Male',
            checkedColor: theme.colors.primary,
          },
          { value: 'female', 
            label: 'Female',
            checkedColor: theme.colors.tertiary,
        },
        ]}
      />

      <Button mode="outlined" onPress={() => navigation.navigate('Settings')}>
      Continue to Video
    </Button>
  </Background>
    );
};

const styles = StyleSheet.create({
    container: {
      flex: 1,
      alignItems: 'center',
    },
    SegmentedButtons: {
      width: '100%',
      marginVertical: 12,
      marginBottom: 200,
    },
  });


export default Welcome;