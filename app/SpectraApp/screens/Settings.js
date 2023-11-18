import React, { memo } from 'react';
import Background from './components/Background';
import TextInput from './components/TextInput';
import Header from './components/Header';
import Paragraph from './components/Paragraph';
import Button from './components/Button';
import { SafeAreaView, StyleSheet } from 'react-native';
import { SegmentedButtons } from 'react-native-paper';
import { theme } from './core/theme';
import AsyncStorage from '@react-native-async-storage/async-storage';

const Welcome = ({navigation}) => {

    const [voice, setVoice] = React.useState('');
    const [phrase, setPhrase] = React.useState('');

    const storeData = async (key, value) => {
        try {
          await AsyncStorage.setItem(key, value);
        } catch (error) {
          console.error('Error storing data:', error);
        }
      };

      const handleSignUp = async () => {
        storeData('phrase', phrase);
        storeData('voice', voice);
        console.log('Data stored');
        navigation.navigate('Video');
    };

return (

  <Background>
    <Header>Action Phrase</Header>
    <Paragraph>
      Set your action phrase to activate Spectra.
    </Paragraph>
    <TextInput
    label= "Action Phrase"
    value={phrase}
    onChangeText={phrase => setPhrase(phrase)}
    />

    <Header>Voice Style</Header>
    <Paragraph>
      Choose a voice style for Spectra.
    </Paragraph>
      <SegmentedButtons style={styles.SegmentedButtons}
        value={voice}
        onValueChange={setVoice}
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

      <Button mode="outlined" onPress={() => handleSignUp()}>
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